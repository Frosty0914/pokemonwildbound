# Testing Notes — InDev 0.0.1

## What to test
Run the generated ROM from a fresh/new save and check:

1. ROM boots normally.
2. Startup/title sequence reaches the Wildbound title presentation.
3. Wildbound/Celebi title graphics render without palette corruption, misplaced tiles, or freezing.
4. Touch/confirm from the title screen proceeds into the new-game intro.
5. Professor Linden graphics render correctly.
6. Intro dialogue advances without broken characters or text-box errors.
7. Male protagonist artwork displays correctly.
8. Name entry can be completed.
9. The intro completes and hands control to the existing placeholder Platinum game world without a crash.
10. Saving/reloading still functions after completing the intro.

## Useful bug report information
When reporting a problem, include:
- emulator or hardware/flashcart used;
- whether you started from a clean save;
- exact screen/line where the problem occurred;
- screenshot if visual;
- whether the issue reproduces after restarting;
- SHA-1 of the generated ROM.

## Expected generated ROM SHA-1
`c75716bfee5b59e83036552727f73477c402005c`

If your hash differs, first verify the base ROM is the exact supported USA Rev 1 dump and that you used the committed assets and builder without editing them.
