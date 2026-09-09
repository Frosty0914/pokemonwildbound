# Known Limitations — InDev 0.0.1

This version intentionally stops before overworld implementation.

- Willowmere Town and its interiors are not implemented. After the intro, the build enters the unchanged Platinum placeholder world.
- Platinum's underlying two-position gender-selection structure has not yet been fully removed at the engine/state-machine level. The visible intro wording is changed and both displayed intro avatars are the male protagonist. If the selector appears, use the default/left choice.
- Celebi is currently implemented as native 2D DS title artwork. Platinum's original 3D Giratina title machinery has not yet been replaced with a custom Celebi animation system.
- The full planned nature/biome opening montage is not yet a complete source-level replacement of every original title/opening effect.
- The Professor's demonstration Pokémon/rival-name portions of Platinum's original new-game logic are not fully redesigned yet.
- This build has been structurally validated and reproduced byte-for-byte by the builder, but emulator/hardware behavior still needs user testing.

These items are development tasks, not intended final behavior.
