import struct
from PIL import Image

def nds_paths(rom):
    fnt_off,fnt_size=struct.unpack_from('<II',rom,0x40); fnt=rom[fnt_off:fnt_off+fnt_size]
    root_sub,root_first,dir_count=struct.unpack_from('<IHH',fnt,0)
    dirs=[struct.unpack_from('<IHH',fnt,i*8) for i in range(dir_count)]
    paths={}
    def parse_dir(di,prefix):
        sub,first,parent=dirs[di]; pos=sub; fid=first
        while True:
            ln=fnt[pos]; pos+=1
            if ln==0: break
            isdir=ln&0x80; n=ln&0x7f
            name=fnt[pos:pos+n].decode('ascii','replace'); pos+=n
            if isdir:
                subid=struct.unpack_from('<H',fnt,pos)[0]; pos+=2
                parse_dir(subid-0xF000,prefix+name+'/')
            else:
                paths[prefix+name]=fid; fid+=1
    parse_dir(0,'')
    return paths

def narc_parse(data):
    if data[:4]!=b'NARC': raise ValueError('not NARC')
    bom,ver,total,hs,secs=struct.unpack_from('<HHIHH',data,4)
    pos=hs; ranges=None; btnf=None; gmif=None
    for _ in range(secs):
        magic=data[pos:pos+4]; size=struct.unpack_from('<I',data,pos+4)[0]; sec=data[pos:pos+size]
        if magic==b'BTAF':
            n=struct.unpack_from('<H',sec,8)[0]; ranges=[struct.unpack_from('<II',sec,12+i*8) for i in range(n)]
        elif magic==b'BTNF': btnf=sec
        elif magic==b'GMIF': gmif=sec[8:]
        pos += size
    return {'bom':bom,'ver':ver,'header_size':hs,'btnf':btnf,'members':[gmif[a:b] for a,b in ranges]}

def narc_build(parsed,members):
    payload=bytearray(); ranges=[]
    for m in members:
        while len(payload)%4: payload.append(0xFF)
        start=len(payload); payload.extend(m); end=len(payload); ranges.append((start,end))
    btaf=bytearray(b'BTAF') + struct.pack('<IHH',12+8*len(members),len(members),0)
    for a,b in ranges: btaf += struct.pack('<II',a,b)
    btnf=parsed['btnf'] or (b'BTNF'+struct.pack('<I',16)+b'\x00'*8)
    gmif=b'GMIF'+struct.pack('<I',8+len(payload))+payload
    total=16+len(btaf)+len(btnf)+len(gmif)
    return bytes(struct.pack('<4sHHIHH',b'NARC',parsed['bom'],parsed['ver'],total,16,3)+btaf+btnf+gmif)

def decode_bank(data):
    num,seed=struct.unpack_from('<HH',data,0); out=[]
    for i in range(num):
        key32=((seed*(i+1)*0x2FD)&0xFFFF) | ((seed*(i+1)*0x2FD0000)&0xFFFF0000)
        eo,es=struct.unpack_from('<II',data,4+i*8); off=eo^key32; sz=es^key32
        key=(0x91BD3*(i+1))&0xFFFF; vals=[]
        for j in range(sz):
            vals.append(struct.unpack_from('<H',data,off+j*2)[0]^key); key=(key+0x493D)&0xFFFF
        out.append(vals)
    return seed,out

def encode_bank(seed,msgs):
    num=len(msgs); hdr=bytearray(4+8*num); struct.pack_into('<HH',hdr,0,num,seed)
    body=bytearray(); cur=len(hdr)
    for i,vals in enumerate(msgs):
        if not vals or vals[-1]!=0xffff: vals=list(vals)+[0xffff]
        key32=((seed*(i+1)*0x2FD)&0xFFFF) | ((seed*(i+1)*0x2FD0000)&0xFFFF0000)
        struct.pack_into('<II',hdr,4+i*8,cur^key32,len(vals)^key32)
        key=(0x91BD3*(i+1))&0xFFFF
        for v in vals:
            body += struct.pack('<H',v^key); key=(key+0x493D)&0xFFFF
        cur += 2*len(vals)
    return bytes(hdr+body)

def textvals(s):
    mp={' ':0x1de,'!':0x1ab,'?':0x1ac,',':0x1ad,'.':0x1ae,"'":0x1b3,':':0x1b1,'-':0x1bd,'é':0x188,'/':0x1c0}
    vals=[]
    for ch in s:
        if ch=='\n': vals.append(0xe000)
        elif ch=='\r': vals.append(0x25bc)
        elif ch=='~': vals.append(0x25bd)
        elif '0'<=ch<='9': vals.append(0x121+ord(ch)-48)
        elif 'A'<=ch<='Z': vals.append(0x12b+ord(ch)-65)
        elif 'a'<=ch<='z': vals.append(0x145+ord(ch)-97)
        elif ch in mp: vals.append(mp[ch])
        else: raise ValueError(('unsupported char',repr(ch)))
    vals.append(0xffff); return vals

def rgb15(c):
    r,g,b=c[:3]; return ((r*31//255)&31)|(((g*31//255)&31)<<5)|(((b*31//255)&31)<<10)

def nscr(b):
    w,h=struct.unpack_from('<HH',b,0x18); size=struct.unpack_from('<I',b,0x20)[0]
    return w,h,list(struct.unpack_from('<'+'H'*(size//2),b,0x24))

def ncgr_info(b):
    assert b[:4]==b'RGCN'
    depth=struct.unpack_from('<I',b,0x1c)[0]
    datasz=struct.unpack_from('<I',b,0x28)[0]
    return depth,0x30,datasz

def encode_layer(gb,pb,sb,target,maxcols=None):
    depth,off,sz=ncgr_info(gb); w,h,ents=nscr(sb); tilebytes=32 if depth==3 else 64; ntiles=sz//tilebytes
    rgba=target.convert('RGBA').resize((w,h),Image.Resampling.NEAREST)
    rgb=Image.new('RGB',(w,h),(0,0,0)); rgb.paste(rgba.convert('RGB'),mask=rgba.getchannel('A'))
    colors=15 if depth==3 else 255
    q=rgb.quantize(colors=colors,method=Image.Quantize.MEDIANCUT)
    pal=q.getpalette()[:colors*3]
    qp=q.load();alpha=rgba.getchannel('A').load(); idx=[[0]*w for _ in range(h)]
    for y in range(h):
        for x in range(w): idx[y][x]=0 if alpha[x,y]<80 else qp[x,y]+1
    tilepix=[None]*ntiles; conflicts=0; cols=w//8
    for i,e in enumerate(ents[:cols*(h//8)]):
        ti=e&0x3ff; hf=(e>>10)&1;vf=(e>>11)&1
        if ti>=ntiles:continue
        tx=(i%cols)*8;ty=(i//cols)*8; arr=[0]*64
        for yy in range(8):
            for xx in range(8):
                sx=7-xx if hf else xx;sy=7-yy if vf else yy
                arr[sy*8+sx]=idx[ty+yy][tx+xx]
        if tilepix[ti] is None: tilepix[ti]=arr
        elif tilepix[ti]!=arr:
            if sum(v!=0 for v in arr)>sum(v!=0 for v in tilepix[ti]): tilepix[ti]=arr
            conflicts+=1
    outg=bytearray(gb); raw=bytearray(sz)
    for ti,arr in enumerate(tilepix):
        if arr is None: arr=[0]*64
        if depth==3:
            for k in range(32): raw[ti*32+k]=(arr[k*2]&15)|((arr[k*2+1]&15)<<4)
        else: raw[ti*64:(ti+1)*64]=bytes(arr)
    outg[off:off+sz]=raw
    outp=bytearray(pb)
    vals=[0]
    for i in range(colors): vals.append(rgb15(tuple(pal[i*3:i*3+3])))
    maxn=min(len(vals),(len(outp)-0x28)//2)
    for i in range(maxn): struct.pack_into('<H',outp,0x28+i*2,vals[i])
    return bytes(outg),bytes(outp),conflicts
