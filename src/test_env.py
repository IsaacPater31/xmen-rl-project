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
    # state=NONE porque todavia no hay un savestate propio (metadata.json esta
    # vacio); arranca desde el power-on de la consola.
    env = retro.make(game=GAME_ID, inttype=retro.data.Integrations.ALL, state=retro.State.NONE)
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
