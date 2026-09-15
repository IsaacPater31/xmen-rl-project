# X-Men: Mutant Apocalypse RL Agent

A reinforcement learning agent that learns to play **X-Men: Mutant Apocalypse** (SNES) on its own, through trial and error.

## Why this project

Years ago I saw my cousin working on something like this with Super Mario, i don't remember exactly what he built or how far he got, but I remember him training some kind of AI to play it, by hand, without any of the tools we have today. That memory stuck with me.

This project is my own take on that idea, using X-Men: Mutant Apocalypse instead of Mario, and modern RL libraries instead of building everything from scratch. It's not meant to be innovative, it's a personal project to understand, end to end, how you actually train an agent that learns by playing, and to document the whole process properly.

## Stack

- **[Stable-Retro](https://github.com/Farama-Foundation/stable-retro)** — emulator that exposes the game state (SNES) as an RL environment.
- **[Stable-Baselines3](https://stable-baselines3.readthedocs.io/)** — pre-implemented RL algorithms (PPO / DQN).
- **TensorBoard** — real-time visualization of training progress.
- **Python 3.10+**

## Project structure

xmen-rl-project/
├── README.md
├── requirements.txt
├── .gitignore
├── roms/            # game ROM not included
├── src/             # project source code
├── docs/
│   ├── bitacora.md  # technical dev log
│   └── capturas/    # screenshots / evidence
├── logs/            # training logs (TensorBoard)
├── models/          # trained models (checkpoints)
└── videos/          # agent evaluation videos

## How to run it

`stable-retro` only ships prebuilt wheels for Linux and macOS — there's no native Windows wheel, and building it from source on Windows would need a full C/C++ toolchain the project isn't even tested against. This is an upstream limitation, not something specific to this repo, so **on Windows the whole workflow runs inside WSL2 (Ubuntu)**, never from PowerShell/cmd directly. On native Linux or macOS you can skip the WSL2 part and just follow from step 3.

### 1. Windows only: install WSL2 (skip if you're on Linux/macOS, or already have it)

If `wsl --status` in PowerShell errors out or shows no distro, install it:

```powershell
wsl --install -d Ubuntu
```

Reboot if asked, then launch "Ubuntu" from the Start menu once to finish setup (it'll ask you to create a Linux username/password — unrelated to your Windows login). Everything from here on happens inside that Ubuntu terminal, not PowerShell.

### 2. Get the project into your Linux/WSL2 shell

If the repo lives on a Windows drive, it's already reachable from WSL2 under `/mnt/<drive>/...`:

```bash
cd /mnt/d/Github/xmen-rl-project   # adjust the drive/path to wherever you cloned it
```

This works fine, but WSL2 bridges the Windows filesystem in a way that's noticeably slower for lots of small file I/O (Python venvs, training logs) than a Linux-native path. If training ever feels I/O-bound, clone the repo into your Linux home instead (`git clone ... ~/xmen-rl-project`) and work from there.

### 3. Set up the Python environment

```bash
bash setup.sh
```

This creates `venv/`, installs `requirements.txt`, and tells you what's next. If it fails asking for `python3-venv` (or a version-specific package like `python3.12-venv`), install exactly the package name it prints, e.g.:

```bash
sudo apt update && sudo apt install -y python3-venv   # match the exact package name from the error
```

then re-run `bash setup.sh`.

In future sessions, just activate the existing environment instead of re-running setup:

```bash
source activate.sh
```

### 4. Add and register the ROM

Not included in this repo (see [`docs/rom-import-notes.md`](docs/rom-import-notes.md) for why and how to get your own) — put it in `roms/`, then register it. Short version: put the ROM file in `roms/`, then try `python -m retro.import roms/`. If it says "Imported 0 games" (true for X-Men: Mutant Apocalypse — see the notes), a custom integration is needed instead; one is already set up for this game under [`src/custom_integrations/`](src/custom_integrations/).

### 5. Install OpenGL system libraries (needed for rendering)

`stable-retro`'s render window depends on `pyglet`, which needs actual OpenGL libraries installed at the system level — a fresh WSL2/Ubuntu install doesn't have them:

```bash
sudo apt update
sudo apt install -y libglu1-mesa freeglut3-dev libgl1
```

Package names shift between Ubuntu versions (e.g. `libgl1-mesa-glx` became `libgl1` on newer releases). If one of these has no installation candidate, run `apt search libglu` / `apt search "^libgl1"` and install whatever matching package your version actually has.

### 6. Test the environment

```bash
python src/test_env.py
```

This should open an emulator window and play random moves until you `Ctrl+C`. If it opens but you don't see a window (headless WSL2, no WSLg) or you get an `ImportError: Library "GLU" not found`, see the troubleshooting notes in [`docs/rom-import-notes.md`](docs/rom-import-notes.md).

## Current status

See [`docs/bitacora.md`](docs/bitacora.md) for the detailed progress log.

