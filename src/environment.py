import os

import stable_retro as retro
from gymnasium.wrappers import TimeLimit

from wrappers import MaxProgressRewardWrapper

# X-Men: Mutant Apocalypse no tiene integracion oficial en stable-retro
# (python -m retro.import no lo reconoce, "Imported 0 games"), asi que usamos
# una integracion custom en custom_integrations/. Ver docs/rom-import-notes.md.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_ID = "XMenMutantApocalypse-Snes"

# Red de seguridad: si por lo que sea "done" no dispara (ej. el frame exacto
# de la muerte se saltea por ruido en la lectura de memoria), un episodio no
# puede quedar corriendo para siempre y arruinar una iteracion de entrenamiento.
MAX_EPISODE_STEPS = 10_000


def register_integration():
    retro.data.Integrations.add_custom_path(os.path.join(SCRIPT_DIR, "custom_integrations"))


def make_env():
    register_integration()
    # state=DEFAULT usa el savestate "Start" declarado en metadata.json,
    # guardado ya con Cyclops dentro de la partida (pasado el intro/menu).
    env = retro.make(game=GAME_ID, inttype=retro.data.Integrations.ALL, state=retro.State.DEFAULT)
    env = TimeLimit(env, max_episode_steps=MAX_EPISODE_STEPS)
    return MaxProgressRewardWrapper(env)
