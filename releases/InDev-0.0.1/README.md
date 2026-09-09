# InDev 0.0.1 — Intro Test

This is the first reproducible Pokémon Wildbound development build.

## Scope

The build is deliberately limited to the opening/title/new-game systems. Willowmere and the rest of the Veyra overworld are not implemented yet.

### Included
- Wildbound title graphics.
- Celebi-themed 2D title presentation.
- Professor Linden intro graphics.
- New male protagonist intro graphics.
- Rewritten introductory Professor dialogue.
- DS-native NCGR/NCLR/NSCR/NARC rebuilding.
- No overworld/map replacement.

## Build it yourself

Requirements:
- Python 3
- Pillow (`pip install -r requirements.txt`)
- A clean Pokémon Platinum USA Rev 1 / v01 ROM.

Required base ROM SHA-1:

`0862ec35b24de5c7e2dcb88c9eea0873110d755c`

From the repository root:

```bash
python tools/build_intro_test.py "/path/to/clean_platinum_rev1.nds" -o "InDev 0.0.1 Intro Test.nds"
```

The builder validates the base ROM before making any changes and writes output checksums and a patch manifest next to the generated ROM.

## Expected output

SHA-1:

`c75716bfee5b59e83036552727f73477c402005c`

SHA-256:

`1f11c87b441b2bf867adfb1260dcd5133922554d3b874637e6aadc05c0acdfd3`

Size: `141815352` bytes.

The GitHub builder and committed DS-ready assets were verified to recreate the original InDev 0.0.1 test ROM byte-for-byte.

## Test goal

Test the flow from boot through title screen and the Professor/new-game sequence into the unchanged placeholder Platinum world. See `TESTING_NOTES.md` and `KNOWN_LIMITATIONS.md` before reporting a problem.
