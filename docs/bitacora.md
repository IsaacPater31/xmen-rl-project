# Dev Log

Technical diary for the project. Each entry: what was tried, what worked, what didn't, and why.

---

## [Date] — Phase 0: Idea and initial setup

**What was done:**
- Defined the project: RL agent for X-Men: Mutant Apocalypse (SNES).
- Created the folder structure (code, docs, logs, models, videos).

**Decisions:**
- Stable-Retro instead of the original Gym Retro (the latter is discontinued).
- Stable-Baselines3 to avoid reinventing the RL algorithms — the focus of this project is the memory mapping and reward function, not implementing PPO from scratch.

**Pending:**
- Install libraries.
- Get the ROM.
- Validate that the game loads correctly in the environment.

---

## [2026-09-14] — Phase 0.1: Windows install failed, pivoted to WSL2

**What was done:**
- Wrote `setup.bat`/`activate.bat` to install dependencies natively on Windows.
- Ran `setup.bat`, which failed while building `stable-retro`.

**What worked:**
- Nothing on the native Windows path — recorded here so I don't retry it later.

**What didn't work / issues:**
- `pip install stable-retro` tried to build from source (`CMake Error: ... CMAKE_C_COMPILER not set`, `Unix Makefiles` generator not available on Windows).
- Root cause: `stable-retro` only publishes wheels for Linux (manylinux) and macOS (arm64) — there is no native Windows wheel, so pip always falls back to a source build on Windows, and the project isn't set up to compile with MSVC anyway.
- Farama's own docs confirm Windows is only supported via WSL2.

**Decisions and why:**
- Moved the whole dev workflow into WSL2 (Ubuntu, already installed on this machine) instead of trying to get a native Windows compiler toolchain working — matches how the project is actually tested upstream, much less fragile than fighting CMake/MSVC.
- Replaced `setup.bat`/`activate.bat` with `setup.sh`/`activate.sh` (bash, run from the WSL shell).

**Screenshots / evidence:** none.

**Pending:**
- Confirm `python src/test_env.py` runs (and renders) correctly from inside WSL2.
- Decide if the repo should move to a native WSL path (`~/...`) instead of `/mnt/d/...` if I/O becomes slow during training.

---

## [2026-09-14] — Phase 0.2: no official integration for the game, built a custom one

**What was done:**
- Installed dependencies successfully from WSL2 (`bash setup.sh`), needed `sudo apt install python3.14-venv` first.
- Ran `python -m retro.import roms/` on the X-Men: Mutant Apocalypse ROM. Result: `Imported 0 games`.
- Checked the installed `stable_retro/data/stable/` folder directly: no `XMen*-Snes` integration exists, only `XMenMojoWorld-Sms` (a different game, different console).
- Built a custom integration by hand at `src/custom_integrations/XMenMutantApocalypse-Snes/`, following `stable_retro`'s own conventions (read from its installed source, `stable_retro/data/__init__.py`, to confirm the ROM must be literally named `rom.<ext>` and how `rom.sha` is formatted).

**What worked:**
- `retro.data.Integrations.add_custom_path(...)` + `inttype=retro.data.Integrations.ALL` + `state=retro.State.NONE` in `retro.make()` is enough to load a game with no metadata/state file at all.

**What didn't work / issues:**
- `retro.import` gives no clear error when the ROM just isn't recognized — it silently reports 0 imports instead of saying "unsupported game", which made it look like the ROM file itself was wrong at first.

**Decisions and why:**
- Going with a custom integration instead of hunting for an alternate ROM/game — X-Men: Mutant Apocalypse is the whole point of the project (the cousin/Mario anecdote), so building the mapping ourselves is expected work, not a blocker to route around.
- `data.json`/`scenario.json` are intentionally empty placeholders for now (reward always 0, no `done` from variables) — good enough to confirm the ROM boots inside the emulator; real memory mapping is separate, larger work.
- The ROM copy inside `custom_integrations/` is gitignored, same as `roms/` — it's still the same copyrighted file, just duplicated for stable-retro's folder convention.

**Screenshots or evidence:** pending — will add once `test_env.py` confirms the render window opens.

**Pending:**
- Confirm `python src/test_env.py` boots the game and renders (still running in WSL2 with WSLg).
- Use the Integration UI (separate GUI app from Farama-Foundation/stable-retro releases) to find real RAM addresses for health/lives/score/position and fill in `data.json` + `scenario.json` for real.
- Create at least one `.state` savestate past the intro/menus so training doesn't restart from the title screen every episode.

---

## [2026-09-14] — Phase 0.3: render confirmed working

**What was done:**
- Ran `python src/test_env.py`. First attempt failed with `ImportError: Library "GLU" not found` — `pyglet` (used by `stable-retro` for rendering) needs system-level OpenGL libraries that a fresh WSL2/Ubuntu install doesn't have.
- Installed `libglu1-mesa`, `freeglut3-dev`, and `libgl1` via `apt` (`libgl1-mesa-glx` from the first attempt had no installation candidate on this Ubuntu version — got renamed to `libgl1`).
- Re-ran `python src/test_env.py`: the emulator window opened and the game renders correctly with random actions.

**What worked:**
- The custom integration (`src/custom_integrations/XMenMutantApocalypse-Snes/`) with empty `data.json`/`scenario.json` and `state=retro.State.NONE` is enough to boot and render the actual game — confirms the whole pipeline (ROM → custom integration → `retro.make()` → render) is wired correctly end to end.

**What didn't work / issues:**
- The missing-library error message didn't obviously point at "install these apt packages" — took inspecting the traceback's own hint (`apt-get install python-opengl`, which is the wrong fix — that's PyOpenGL, not the system `libGLU.so`) plus knowing WSL2/Ubuntu minimal installs skip GL libraries entirely.

**Decisions and why:**
- Documented both the WSLg troubleshooting and this separate OpenGL-libraries troubleshooting as two distinct sections in `docs/rom-import-notes.md`, since they look similar ("nothing renders") but have unrelated causes and fixes — worth keeping apart for future setups on a new machine.

**Screenshots or evidence:** none yet — will add a screenshot to `docs/capturas/` next time.

**Pending:**
- Use the Integration UI to find real RAM addresses (health/lives/score/position) and fill in `data.json` + `scenario.json` for a real reward signal.
- Create at least one `.state` savestate past the intro/menus so training doesn't restart from the title screen every episode.
- Once there's a real reward signal, write the first PPO training script with Stable-Baselines3.

---

## [2026-09-15] — Phase 1: built the Integration UI and mapped real memory addresses

**What was done:**
- Discovered the Integration UI isn't distributed as a binary anywhere (GitHub releases have no assets) — it has to be compiled from Stable-Retro's full C++ source with Qt5, completely separate from the pip package/venv.
- Cloned `Farama-Foundation/stable-retro` into `~/stable-retro-src` (outside the project repo) and built it with `cmake . -DBUILD_UI=ON -UPYLIB_DIRECTORY` + `make -j$(nproc)`.
- Installed everything the build needed, in order, as each missing piece surfaced: `build-essential cmake capnproto libcapnp-dev libqt5opengl5-dev qtbase5-dev zlib1g-dev` (from the official docs), then `python3-dev pkg-config libbz2-dev` (not documented anywhere, but required — `cmake` failed on `_Python_INCLUDE_DIR-NOTFOUND` without `python3-dev`).
- Opened `./gym-retro-integration`, loaded the ROM directly (`File → Open...`), played manually with the default keyboard mapping (arrows, Z/X/A/S, Enter for Start) to get past the intro into actual gameplay as Cyclops.
- Saved a savestate (`Start.state`) right after entering gameplay, moved it into `src/custom_integrations/XMenMutantApocalypse-Snes/Start.state`, and pointed `metadata.json`'s `default_state` at it. Updated `test_env.py` to load with `state=retro.State.DEFAULT` instead of `State.NONE`.
- Used the Search panel (`Window → Show search...`) to hunt for the player's health address: seeded a search, then alternated `Unchanged` (when nothing happened) and `Decreased` (right after taking a confirmed hit) to kill off noise from unrelated addresses (timers, animation counters) instead of just spamming `Decreased`, which too easily zeroes out all candidates.
- Cross-referenced with a [TASVideos forum post](https://tasvideos.org/Forum/Topics/1584?CurrentPage=2) that shares a RAM-watch list for this exact game (enemy/boss HP, player position/speed) — verified by fetching the actual page content, not taken on faith.

**What worked:**
- **`health`** → `0x7E0C35` (`<u2`): confirmed empirically — drops with each hit (63 → 1 near death), hits exactly 0 on death. Some flicker between 0 and 63 right at the lethal hit (looks like a death-animation/invincibility-blink artifact), accepted as noise for now.
- **`pos_x`** → `0x7E0C05` (`<u2`), from the TASVideos list: confirmed by walking right (increases) and left (decreases, floors around 20).
- **`pos_y`** → `0x7E0C08` (`<u2`), from the TASVideos list: confirmed by jumping (decreases going up, as expected for screen coordinates).
- Wrote the first real `data.json` (all 3 variables above) and `scenario.json` (`done` when `health == 0`; reward: penalty on `health` decreasing, reward on `pos_x` increasing) in `src/custom_integrations/XMenMutantApocalypse-Snes/`, replacing the empty placeholders from Phase 0.2.

**What didn't work / issues:**
- First guess for "lives" — `0x7E0C34`, a byte that happened to read `2` once — turned out to be unrelated character/animation state: it changed on movement and on getting hit (jumping to values like 5 or 8), not just on losing a life. Dropped it; not needed anyway, since the RL environment just treats every death as an episode reset regardless of the game's own lives counter.
- A separate, unrelated delta-search (candidates around `0x78E`/`0x793`, large values like 4605240/14707808) was a red herring — most likely a frame counter or similar, not tied to player state at all.
- Found by accident that `0x7E0C33`/`0x7E0C34`, read as multi-digit BCD (`Repr::BCD = 'd'` in Stable-Retro's own `memory.h`), shows values consistent with an internal **score** counter (200, 20000, 2000000 depending on how many BCD digits you read) — contradicts the earlier research guess that this game has no score. Not used in the reward yet; noted for later.

**Decisions and why:**
- Kept `data.json`/`scenario.json` deliberately minimal (health + x-position only) instead of also wiring up enemy/boss HP — the TASVideos-sourced enemy addresses are unverified by us, and the point of this phase was getting *something* real and self-verified working end to end, not a complete reward function on the first pass.
- Documented the Integration UI build's full dependency list in the README so a clean machine doesn't have to rediscover `python3-dev`/`pkg-config`/`libbz2-dev` the hard way like we did.

**Screenshots or evidence:** none yet — pending a capture of the Integration UI mid-search for `docs/capturas/`.

**Pending:**
- Verify/use the score address (`0x7E0C33`, BCD) if it turns out useful for the reward.
- Consider whether to also map enemy/boss HP now that we know the workflow, or move straight to a first PPO training run with what we have.
- First PPO training script with Stable-Baselines3, using the `feature/reward-mapping` work once merged.

---

## Template for future entries

## [Date] — Phase X: [phase name]

**What was done:**
-

**What worked:**
-

**What didn't work / issues:**
-

**Decisions and why:**
-

**Screenshots / evidence:** (link to `docs/capturas/` or `videos/`)

**Pending:**
-