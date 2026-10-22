# Lab 5 – Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the style issues from Flake8 and Pylint: removing the unused `json` import, renaming `l` to `top`, changing `== None` to `is None`, wrapping long lines and renaming functions to snake_case. Each is a mechanical, local change that the tool points to exactly.

The hardest were the Bandit security issues and the global connection warning, because they needed understanding of *why* the code was unsafe rather than just how to silence the warning. For the SQL injection I had to switch to parameterised queries instead of just reformatting the string. For `os.system` I had to decide the shell wasn't needed at all. Fixing `redefined-outer-name` meant restructuring the program so the connection is created inside `main()` and passed into functions, which touched every function.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Mostly the findings were genuine, but a couple are context-dependent. Bandit's B324 MD5 warning is a true positive in principle, but if the hash were only used as a non-secret lookup key, `usedforsecurity=False` would have been an acceptable fix; here I chose SHA-256 because a farmer token could be treated as an identifier. Some overlap also exists: Flake8 E501 (79 chars) and Pylint C0301 (100 chars) flag the same lines with different limits, and both tools report the unused import. Conversely, none of the tools caught the real runtime bug that `top_farmer()` crashes on an empty table, which shows static analysis has false negatives too.

**3. How would you integrate static analysis tools into your actual software development workflow?**

- Run Flake8 and Pylint in the editor (VS Code / PyCharm plugins) for instant feedback while coding.
- Add a `pre-commit` hook running Flake8, Pylint and Bandit so issues are caught before each commit.
- Run all three in CI (e.g. GitHub Actions) on every pull request, failing the build on any Bandit High/Medium issue, any Flake8 error, or a Pylint score below a threshold such as 9.5.
- Keep shared configuration (`.pylintrc`, `setup.cfg` / `.flake8`) in the repo so the whole team uses the same rules, and document any deliberate `# nosec` or `# pylint: disable` with a reason.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

- **Security:** all three Bandit issues were removed — no SQL injection, no shell injection, no weak hashing (High 2 → 0, Medium 1 → 0).
- **Quality score:** Pylint went from 2.00/10 to 10.00/10, and Flake8 from 7 issues to 0.
- **Readability:** consistent snake_case names, docstrings on every function, f-strings and a named constant `LOW_FAT_THRESHOLD` make the intent clear.
- **Robustness and reuse:** the module no longer opens a database or runs the demo on import, the connection is closed properly, and `top_farmer()` no longer crashes when there is no data. The program still produces the same results as before.
