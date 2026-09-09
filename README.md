# Pokémon Wildbound: A Platinum ROM Hack

**Pokémon Wildbound** is an in-development ROM hack based on **Pokémon Platinum (USA Rev 1)**. It is designed as a new Gen 4-style Pokémon adventure set in the original Veyra region, with an ecology/nature theme, a 180-species regional Pokédex drawn from Generations 1–4, eight new Gyms, Team Verdant, and Celebi at the center of the Wildheart storyline.

## Current version

**InDev 0.0.1 — Intro Test**

This first development build focuses only on the startup experience:

- Wildbound-branded title graphics
- Celebi-focused title presentation
- Professor Linden intro assets
- male-only player concept/intro assets
- early new-game intro modifications
- DS-native graphics conversion/rebuild work

World-map replacement and Willowmere are intentionally **not** part of 0.0.1.

## How builds are distributed

This repository does **not** distribute Pokémon Platinum ROM files or complete modified `.nds` files. Development builds are distributed as patches that must be applied to a legally obtained clean copy of the supported base ROM.

Target base:

- Pokémon Platinum Version
- USA
- Rev 1 / v01
- SHA-1: `0862ec35b24de5c7e2dcb88c9eea0873110d755c`

See the release folder for checksums and testing notes.

## Project goals

- Native Generation 4 mechanics and presentation
- 150–200 Pokémon regional Pokédex (currently 180)
- Pokémon from Generations 1–4 only
- No Fakemon or regional forms
- Standard official-game difficulty
- Minimal grinding
- Roughly 15–20 hour main story
- New Veyra region with plains, forests, lakes, coast, wetlands, desert, mountains and tundra
- Team Verdant environmental-extremist storyline
- Eight Gyms, Elite Four and Champion

## Repository layout

- `data/` — regional Dex, encounters, progression and trainer design data
- `docs/` — implementation notes and technical planning
- `tools/` — project/build helper scripts
- `releases/` — patch files and release-specific documentation

## Development workflow

`main` is the stable development branch. Larger features should be built on branches such as `feature/willowmere` and merged back after testing. Test builds use the `InDev` version scheme.

## Development status

The project is in very early development. `InDev 0.0.1` is an intro/title technical test, not a playable story demo.

## Legal

Pokémon and Pokémon Platinum are trademarks/copyrights of their respective owners. This is an unofficial non-commercial fan project. No original Nintendo ROM is included in this repository.
