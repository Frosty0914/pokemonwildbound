# Veyra Platinum Implementation Notes

## Base ROM
- Target: Pokémon Platinum Version, North American Rev 1 (`CPUE`, revision 1).
- Required SHA-1: `0862ec35b24de5c7e2dcb88c9eea0873110d755c`.
- The project deliberately keeps all native Gen 4 personal data: base stats, types, catch rates, growth rates, abilities, learnsets, evolution mechanics, and the Gen 4 battle engine.

## What the included mechanics prototype changes
The builder patches the supplied ROM's encounter and trainer NARCs only. It creates a **mechanics/balance sandbox**, not the final Veyra overworld.

1. `fielddata/encountdata/pl_enc_data.narc`: selected Sinnoh encounter entries are replaced with Veyra habitat tables and the intended level curve.
2. `poketool/trainer/trdata.narc` + `trpoke.narc`: vanilla Gym/E4/Champion trainer IDs are replaced with the designed Veyra boss rosters. Selected Team Galactic boss IDs are replaced with Briar/Calder/Vale rosters. Galactic male/female grunt classes are given Team Verdant-style species pools while preserving their original levels and party sizes.
3. Pokémon personal data is **not modified**.
4. The native Turtwig/Chimchar/Piplup starter logic is retained.
5. Text, scripts, map geometry, trainer sprites, overworld sprites, and custom 3D maps are intentionally not misrepresented as finished in the prototype.

## Why the custom overworld is a separate build layer
A true Platinum-region replacement requires DS map/model assets, terrain/collision, map headers, world matrices, events, scripts, warps, and text. The map manifest in this pack specifies the intended topology and scope. Build the custom map layer in Pokémon DS Map Studio and import/integrate it with DSPRE, then apply the encounter/trainer data in this pack.

## Prototype encounter index mapping
The JSON encounter data records the vanilla `pl_enc_data.narc` entries used as test beds. These let the level curve and species ecology be play-tested in the existing Sinnoh geometry before final Veyra maps are compiled.

## Final build order
1. Build/import Willowmere, Cedarbrook, Route 1, Route 2, and Meadowgate as the vertical slice.
2. Script opening, starter, rival, first Verdant protest, and Gym 1.
3. Add Verdant Forest/Alderwood and Granite Hollow; validate early pacing and no-grind level curve.
4. Expand sequentially through Lakehurst -> Seabreak -> Mirehaven -> Suncleft -> Eastcrest/Frostveil/Wildheart -> Cragspire -> Victory Road/League.
5. Replace placeholder trainer/overworld graphics with the DS-style Team Verdant/Gym/E4 assets.
6. Complete text, map-name tables, Fly destinations, Pokédex regional ordering, postgame Wild Frontier, and final QA.

## Regional Dex
Exactly 180 species. Every Gym, Elite Four, Champion, and Team Verdant boss Pokémon is included. Major special acquisitions are documented in `veyra_regional_dex.csv`.

## Design constraint
Do not expand this project with later-generation mechanics or species unless the design is explicitly changed. It is intended to feel like an original Gen 4 DS game.
