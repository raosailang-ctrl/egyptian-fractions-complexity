# Applying this repository update

This ZIP is an overlay update, not a replacement copy of the entire repository. It contains the files changed for the fixed-prime numerator research update.

1. Extract the ZIP.
2. Copy the files inside `egyptian-fractions-complexity-update/` into the root of your existing `egyptian-fractions-complexity` working folder, allowing the listed Markdown files to be replaced.
3. Keep the existing `.git` folder and all files not included in this update. Do not delete the existing repository contents.
4. Run the verifier from the repository root:

       python fixed-prime-dp.py

5. Review the output, then commit and push the update:

       git add .
       git commit -m "Add fixed-prime numerator CRT dynamic programming"
       git push

The archive deliberately does not overwrite `mathematical-foundations.md`, `randomized-reduction.md`, `minimum-term-decision.md`, `references.md`, or the earlier signed-reduction scripts. Those files remain part of the existing repository.
