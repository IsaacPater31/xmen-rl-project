from environment import make_env


def run_random_agent(env):
    env.reset()
    episode = 1
    episode_reward = 0.0
    while True:
        action = env.action_space.sample()
        _obs, reward, terminated, truncated, info = env.step(action)
        episode_reward += reward
        env.render()

        health = info.get("health")
        pos_x = info.get("pos_x")
        print(
            f"\rEp {episode} | reward paso: {reward:+7.2f} | acumulado: {episode_reward:+9.2f} "
            f"| health: {health} | pos_x: {pos_x}   ",
            end="",
            flush=True,
        )

        if terminated or truncated:
            print(f"\nEpisodio {episode} terminado, reward acumulado: {episode_reward:.2f}")
            episode += 1
            episode_reward = 0.0
            env.reset()


def test_env():
    env = make_env()
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
