# ROM notes

## Legal note

This repo does **not** include or distribute the game ROM. Get your own copy from a cartridge/console you legally own and place the file yourself — the project just documents where it goes and what to do with it.

## Steps

1. Put the ROM file (`.sfc` or `.smc`) in the `roms/` folder.
2. Run Stable-Retro's importer pointing at that folder:

   ```bash
   python -m retro.import roms/
   ```

3. If the game has an official Stable-Retro integration, the command prints the id it registered (e.g. `AeroTheAcroBat-Snes`). Copy that exact id into the `GAME_ID` constant in [`src/test_env.py`](../src/test_env.py).

## If it's not recognized ("Imported 0 games")

**This is what happens with X-Men: Mutant Apocalypse** — it has no official Stable-Retro integration (confirmed by checking the installed `stable_retro/data/stable/` folder: there's no `XMen*-Snes` at all, only `XMenMojoWorld-Sms`, a different game on a different console). When this happens, `retro.import` doesn't error out — it just doesn't find your ROM's hash in its internal database and reports "Imported 0 games".

The fix is to build a **custom integration** by hand instead of going through `retro.import`. That's already set up in this project, under [`src/custom_integrations/XMenMutantApocalypse-Snes/`](../src/custom_integrations/XMenMutantApocalypse-Snes/):

```
src/custom_integrations/
└── XMenMutantApocalypse-Snes/    # <GameName>-<System>, no spaces
    ├── rom.sfc                   # the ROM, renamed literally to rom.<ext> (NOT committed to git)
    ├── rom.sha                   # lowercase SHA1 of the ROM + trailing newline
    ├── data.json                 # memory addresses (empty for now)
    ├── scenario.json             # reward / done conditions (empty for now)
    └── metadata.json             # starting state (empty; test_env.py uses state=retro.State.NONE)
```

Key points, confirmed by reading Stable-Retro's own installed source (`stable_retro/data/__init__.py`):

- The ROM file **must** be named exactly `rom.<extension>` (`rom.sfc` for SNES) — that's how Stable-Retro looks it up internally (`get_romfile_path`), regardless of the file's original name.
- `rom.sha` is the output of `sha1sum rom.sfc` (or the original file), keeping only the lowercase hash — not the filename `sha1sum` appends after it.
- `src/test_env.py` registers the folder with `retro.data.Integrations.add_custom_path(...)` and passes `inttype=retro.data.Integrations.ALL` to `retro.make()` so it gets picked up.
- `data.json`/`scenario.json` are intentionally empty right now: the environment loads and renders fine, but reward is always 0 and episodes never end from variables (only from a step limit, if one exists). That's enough to confirm the ROM boots correctly.

### Pending: mapping real memory

For the RL agent to get a real reward signal, `data.json` (memory addresses — lives, health, score, position, etc.) and `scenario.json` (which variables give reward and which one ends the episode) need to be filled in for real. That means exploring the game's RAM with Stable-Retro's **Integration UI** — a separate GUI app, not part of the pip package, downloaded from the [Farama-Foundation/stable-retro](https://github.com/Farama-Foundation/stable-retro) GitHub releases.

## Troubleshooting: `ImportError: Library "GLU" not found`

This means the display side (WSLg) is fine, but the Linux system itself is missing the actual OpenGL libraries `pyglet` links against — a bare WSL2/Ubuntu install doesn't ship them. Fix:

```bash
sudo apt update
sudo apt install -y libglu1-mesa freeglut3-dev libgl1
```

If a package name doesn't exist on your Ubuntu version (they get renamed across releases — e.g. `libgl1-mesa-glx` → `libgl1`), find the current name with `apt search libglu` / `apt search "^libgl1"` and install that instead.

## Troubleshooting: no render window on WSL2

`env.render()` needs a display. On Windows 11, WSL2 ships with WSLg (GUI app forwarding) enabled by default, so a window should just appear. If it doesn't:

- Update WSL from PowerShell: `wsl --update`, then restart WSL (`wsl --shutdown`, reopen the Ubuntu terminal).
- Check `echo $DISPLAY` inside WSL — it should print something like `:0`. If it's empty, WSLg isn't wired up for that session; restarting WSL (above) usually fixes it.
- Confirm you're on Windows 11 (or Windows 10 with WSLg backported) — on older Windows 10 builds without WSLg, GUI apps from WSL2 don't have anywhere to render at all, and you'd need a separate X server (e.g. VcXsrv) as a workaround.
