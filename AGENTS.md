# AGENTS.md

## Sadr

### Build and test
- The repo has no tests. Run `uv sync --locked`, then `uv run python -m py_compile code.py dino.py sounds.py generate_sprites.py`. Passing means both exit 0.
- Run `uv run python generate_sprites.py`. It rewrites `sprites/*.bmp` in place. Passing means `git status` shows no change to `sprites/`.
- `code.py`, `dino.py` and `sounds.py` import CircuitPython modules such as `board` and `adafruit_magtag`. They run only on an Adafruit MagTag, so the host can only compile them.

### Toolchain
- `pyproject.toml` and `uv.lock` cover only the host tool `generate_sprites.py`, which needs Pillow. The MagTag code uses CircuitPython bundle libraries that the README tells users to copy by hand. The repo pins none of them.
