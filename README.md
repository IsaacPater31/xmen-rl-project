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

```
xmen-rl-project/
├── README.md
├── requirements.txt
├── .gitignore
├── roms/            # ROM del juego (no incluida, ver nota legal)
├── src/             # Código fuente del proyecto
├── docs/
│   ├── bitacora.md  # Diario técnico de desarrollo
│   └── capturas/    # Capturas de pantalla / evidencia
├── logs/            # Logs de entrenamiento (TensorBoard)
├── models/          # Modelos entrenados (checkpoints)
└── videos/          # Videos de evaluación del agente
```

## How to run it

_(fills in as the project progresses)_

## Current status

See [`docs/bitacora.md`](docs/bitacora.md) for the detailed progress log.

