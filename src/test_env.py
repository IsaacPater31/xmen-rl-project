import os

import stable_retro as retro

# X-Men: Mutant Apocalypse no tiene integracion oficial en stable-retro
# (python -m retro.import no lo reconoce, "Imported 0 games"), asi que usamos
# una integracion custom en custom_integrations/. Ver docs/rom-import-notes.md.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_ID = "XMenMutantApocalypse-Snes"

retro.data.Integrations.add_custom_path(os.path.join(SCRIPT_DIR, "custom_integrations"))


def run_random_agent(env):
    env.reset()
    while True:
        action = env.action_space.sample()
        _obs, _reward, terminated, truncated, _info = env.step(action)
        env.render()
        if terminated or truncated:
            env.reset()


def test_env():
    # state=DEFAULT usa el savestate "Start" declarado en metadata.json,
    # guardado ya con Cyclops dentro de la partida (pasado el intro/menu).
    env = retro.make(game=GAME_ID, inttype=retro.data.Integrations.ALL, state=retro.State.DEFAULT)
    try:
        run_random_agent(env)
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario, cerrando entorno...")
    finally:
        env.close()


def main():
    test_env()


if __name__ == "__main__":
    main()
