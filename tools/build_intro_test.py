from pathlib import Path
import struct, hashlib, json, sys, argparse
from PIL import Image
from wildbound_nds import nds_paths, narc_parse, narc_build, decode_bank, encode_bank, textvals, rgb15, nscr, ncgr_info, encode_layer

EXPECTED_BASE_SHA1='0862ec35b24de5c7e2dcb88c9eea0873110d755c'

parser=argparse.ArgumentParser(description='Build Pokémon Wildbound InDev 0.0.1 Intro Test from a clean Platinum USA Rev 1 ROM.')
parser.add_argument('base_rom',type=Path)
parser.add_argument('-o','--output',type=Path,default=Path('InDev 0.0.1 Intro Test.nds'))
args=parser.parse_args()
BASE=args.base_rom; OUTROM=args.output
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'/'indev-0.0.1'
if not BASE.exists(): raise SystemExit(f'Base ROM not found: {BASE}')
base_bytes=BASE.read_bytes(); base_sha1=hashlib.sha1(base_bytes).hexdigest()
if base_sha1 != EXPECTED_BASE_SHA1:
    raise SystemExit(f'Wrong base ROM SHA-1: {base_sha1}\nExpected: {EXPECTED_BASE_SHA1}')
rom=bytearray(base_bytes)
paths=nds_paths(rom)
fat_off=struct.unpack_from('<I',rom,0x48)[0]

def get_file(fid):
    s,e=struct.unpack_from('<II',rom,fat_off+fid*8); return bytes(rom[s:e])

def replace_file(fid,data):
    global rom
    pos=(len(rom)+0x1ff)&~0x1ff
    if pos>len(rom): rom.extend(b'\0'*(pos-len(rom)))
    rom.extend(data)
    struct.pack_into('<II',rom,fat_off+fid*8,pos,pos+len(data))
    return (pos,pos+len(data))

text_replacements={
0:"Hello there!\nWelcome to the world of Pokémon!\r",
1:"My name is Professor Linden.\rPeople call me the Pokémon Professor.\rI study Pokémon and the places\nthey call home.\r",
10:"You are about to enter a world\nshaped by forests, rivers, mountains,\nand seas.\r",
11:"Everywhere you travel, people and\nPokémon share the land together.\rSpeak to everyone you meet, and\nlook closely at the world around you.\r",
12:"New paths will open as you help\nothers, face challenges, and uncover\nthe mysteries of this region.\r",
14:"But a journey is about more than\nbecoming powerful.\r",
15:"Meet many Pokémon. Meet many people.\rLearn from the places you visit,\nand decide what kind of Trainer\nyou want to become.\r",
16:"This world is widely inhabited by\ncreatures known as Pokémon.\r",
19:"We humans live alongside Pokémon\nas friends and partners.\rSometimes we play together. At other\ntimes we work together or battle.\rMy research asks a simple question:\nhow do Pokémon, people, and their\nenvironments shape one another?\r",
20:"Now, I'd like to know a little\nabout you.\r",
21:"There you are.\nReady to begin?\r",
22:"Good. Let's continue.\r",
23:"Good. Let's continue.\r",
24:"And what is your name?\r",
}
text_patch_info=[]
for narcpath,member in [('msgdata/pl_msg.narc',389),('msgdata/msg.narc',341)]:
    fid=paths[narcpath]; parsed=narc_parse(get_file(fid)); members=list(parsed['members'])
    seed,msgs=decode_bank(members[member])
    for idx,s in text_replacements.items(): msgs[idx]=textvals(s)
    members[member]=encode_bank(seed,msgs)
    newn=narc_build(parsed,members); replace_file(fid,newn)
    text_patch_info.append({'archive':narcpath,'member':member,'messages':sorted(text_replacements)})

intro_fid=paths['demo/intro/intro.narc']; ip=narc_parse(get_file(intro_fid)); imems=list(ip['members'])
prof_target=Image.open(ASSETS/'professor_linden_ds_layer.png').convert('RGBA')
player_target=Image.open(ASSETS/'male_player_ds_layer.png').convert('RGBA')
if prof_target.size != (256,192) or player_target.size != (256,192):
    raise SystemExit('Intro assets must be 256x192 PNGs.')
ng,npal,c1=encode_layer(imems[19],imems[20],imems[23],prof_target)
imems[19]=ng;imems[20]=npal
ng,npal,c2=encode_layer(imems[9],imems[13],imems[23],player_target)
for n in [9,10,11,12]:
    tmp=bytearray(imems[n]); depth,off,sz=ncgr_info(tmp); _,off2,sz2=ncgr_info(ng)
    tmp[off:off+min(sz,sz2)]=ng[off2:off2+min(sz,sz2)]; imems[n]=bytes(tmp)
imems[13]=npal
for dst,src in zip([14,15,16,17],[9,10,11,12]): imems[dst]=imems[src]
imems[18]=imems[13]
new_intro=narc_build(ip,imems); replace_file(intro_fid,new_intro)

title_fid=paths['demo/title/titledemo.narc']; tp=narc_parse(get_file(title_fid)); tmem=list(tp['members'])
interim_title=Image.open(ASSETS/'wildbound_title_ds_layer.png').convert('RGBA')
if interim_title.size != (256,256): raise SystemExit('Interim title asset must be 256x256 PNG.')
ng,npal,c3=encode_layer(tmem[12],tmem[11],tmem[28],interim_title)
tmem[12]=ng; tmem[11]=npal
replace_file(title_fid,narc_build(tp,tmem))

title_fid=paths['demo/title/titledemo.narc']; tp=narc_parse(get_file(title_fid)); tmem=list(tp['members'])
canvas=Image.open(ASSETS/'wildbound_title_target.png').convert('RGBA')
if canvas.size != (256,256): raise SystemExit('Title target must be 256x256 PNG.')
rgb=Image.new('RGB',canvas.size,(0,0,0)); rgb.paste(canvas.convert('RGB'),mask=canvas.getchannel('A'))
q=rgb.quantize(colors=255,method=Image.Quantize.MEDIANCUT); pal=q.getpalette()[:765]; qp=q.load(); ap=canvas.getchannel('A').load()
idx=[[0]*256 for _ in range(256)]
for y in range(256):
    for x in range(256): idx[y][x]=0 if ap[x,y]<80 else qp[x,y]+1
screen=bytearray(tmem[28]); sw,sh=struct.unpack_from('<HH',screen,0x18); size=struct.unpack_from('<I',screen,0x20)[0]
if (sw,sh)!=(256,256): raise SystemExit('Unexpected Platinum title screen-map dimensions.')
ents=[0]*(size//2); tiledata=[bytes(64)]; nexti=1
for ty in range(sh//8):
    for tx in range(sw//8):
        arr=bytes(idx[ty*8+yy][tx*8+xx] for yy in range(8) for xx in range(8)); pos=ty*(sw//8)+tx
        if any(arr):
            if nexti>=512: raise SystemExit(f'Title exceeds tile budget: {nexti}')
            ents[pos]=nexti; tiledata.append(arr); nexti+=1
for i,e in enumerate(ents): struct.pack_into('<H',screen,0x24+i*2,e)
nc=bytearray(tmem[12]); ds=struct.unpack_from('<I',nc,0x28)[0]
if ds<512*64: raise SystemExit('Unexpected title NCGR size.')
raw=b''.join(tiledata)+bytes((512-len(tiledata))*64); nc[0x30:0x30+512*64]=raw[:512*64]
pb=bytearray(tmem[11]); vals=[0]+[rgb15(tuple(pal[i:i+3])) for i in range(0,len(pal),3)]
for i,v in enumerate(vals[:256]): struct.pack_into('<H',pb,0x28+i*2,v)
tmem[12]=bytes(nc); tmem[11]=bytes(pb); tmem[28]=bytes(screen)
replace_file(title_fid,narc_build(tp,tmem))

OUTROM.parent.mkdir(parents=True,exist_ok=True)
OUTROM.write_bytes(rom)
vrom=OUTROM.read_bytes(); vpaths=nds_paths(vrom)
def vf(p):
    fid=vpaths[p]; fo=struct.unpack_from('<I',vrom,0x48)[0]
    s,e=struct.unpack_from('<II',vrom,fo+fid*8); return vrom[s:e]
for p in ['demo/intro/intro.narc','demo/title/titledemo.narc','msgdata/pl_msg.narc','msgdata/msg.narc']:
    narc_parse(vf(p))
sha1=hashlib.sha1(vrom).hexdigest(); sha256=hashlib.sha256(vrom).hexdigest()
manifest={
    'version':'InDev 0.0.1 Intro Test',
    'base_sha1':base_sha1,
    'output_sha1':sha1,
    'output_sha256':sha256,
    'modified_nitrofs':['demo/intro/intro.narc','demo/title/titledemo.narc','msgdata/pl_msg.narc','msgdata/msg.narc'],
    'world_maps_modified':False,
    'emulator_tested':False
}
(OUTROM.parent/'PATCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(OUTROM.parent/'CHECKSUMS.sha1').write_text(f'{sha1}  {OUTROM.name}\n',encoding='utf-8')
(OUTROM.parent/'CHECKSUMS.sha256').write_text(f'{sha256}  {OUTROM.name}\n',encoding='utf-8')
print(f'Built: {OUTROM}')
print(f'SHA-1: {sha1}')
print(f'SHA-256: {sha256}')
