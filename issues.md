# Lab 5 – Issues Found and Fixed (`dairy_collection.py`)

Baseline: Pylint **2.00/10**, Bandit **3 issues** (2 High, 1 Medium), Flake8 **7 issues**.
After fixes: Pylint **10.00/10**, Bandit **0 issues**, Flake8 **0 issues**.

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Shell command injection | Bandit B605 (CWE-78) | Security | High | 31 | `os.system("echo printing slip for " + farmer)` passes user data to a shell; a name like `x; rm -rf ~` would run a command. | Removed the shell call and used `print()` directly; dropped the now-unused `import os`. |
| 2 | Weak hash (MD5) | Bandit B324 (CWE-327) | Security | High | 16 | MD5 is broken and collision-prone, unsafe for any identifying token. | Replaced `hashlib.md5` with `hashlib.sha256`. |
| 3 | SQL injection | Bandit B608 (CWE-89) | Security | Medium | 11 | INSERT built with `str.format()`; a farmer name containing `'` breaks the query or injects SQL. | Used a parameterised query with `?` placeholders and a values tuple. |
| 4 | Global DB connection shadowed | Pylint W0621 | Design / Bug-risk | Medium | 6, 10, 19, 24, 34 | Module-level `conn` is redefined by every function parameter; connection is created on import. | Moved creation into `create_db()`, called from `main()`; connection closed at the end. |
| 5 | Code runs on import | Pylint (design) | Design | Medium | 47 | `main()` called unconditionally, so importing the module runs the demo. | Wrapped in `if __name__ == "__main__":`. |
| 6 | `== None` comparison | Flake8 E711 / Pylint C0121 | Bug-risk | Medium | 36 | `fat == None` can misbehave with objects overriding `__eq__`. | Changed to `fat is None`. |
| 7 | Unused import | Flake8 F401 / Pylint W0611 | Quality | Low | 2 | `json` imported but never used. | Removed the import. |
| 8 | Ambiguous variable name | Flake8 E741 | Style | Low | 26 | `l` is easily confused with `1`/`I`. | Renamed to `top`. |
| 9 | Lines too long | Flake8 E501 / Pylint C0301 | Style | Low | 7, 11, 20, 25 | Lines exceed 79 (PEP 8) / 100 (Pylint) characters. | Split SQL strings and calls across lines. |
| 10 | Non-snake_case names | Pylint C0103 | Style | Low | 10, 15, 19, 24, 30, 34 | `recordMilk`, `farmerToken`, etc. break PEP 8 naming. | Renamed to `record_milk`, `farmer_token`, `daily_total`, `top_farmer`, `print_slip`, `low_fat`. |
| 11 | Missing docstrings | Pylint C0114 / C0116 | Documentation | Low | 1, all functions | No module or function docstrings. | Added a module docstring and one per function. |
| 12 | Old-style `%`/`.format` strings | Pylint C0209 | Style | Low | 11, 21 | Could be f-strings. | Used f-strings (`f"Total: {total:.1f} litres"`). |
| 13 | Crash on empty table *(found while fixing, not reported by tools)* | Manual review | Bug | Medium | 26 | `max()` on an empty result raises `ValueError`. | `top_farmer()` returns `None` when there is no data. Also replaced magic number `3.5` with `LOW_FAT_THRESHOLD`. |

The program output is unchanged except the farmer token, which is now a 64-character SHA-256 hash instead of a 32-character MD5 hash.
