import os
from dataclasses import dataclass

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.monitor import Monitor

from environment import make_env

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")


@dataclass
class TrainingConfig:
    total_timesteps: int = 200_000
    checkpoint_freq: int = 10_000
    model_name: str = "ppo_xmen_cyclops"


def build_env() -> Monitor:
    return Monitor(make_env())


def build_model(env, config: TrainingConfig) -> PPO:
    model_path = os.path.join(MODELS_DIR, f"{config.model_name}.zip")
    if os.path.exists(model_path):
        print(f"Retomando modelo guardado en {model_path}")
        return PPO.load(model_path, env=env, tensorboard_log=LOGS_DIR)
    return PPO("CnnPolicy", env, verbose=1, tensorboard_log=LOGS_DIR)


def build_checkpoint_callback(config: TrainingConfig) -> CheckpointCallback:
    return CheckpointCallback(
        save_freq=config.checkpoint_freq,
        save_path=MODELS_DIR,
        name_prefix=config.model_name,
    )


def train_model(model: PPO, config: TrainingConfig, callback: CheckpointCallback) -> None:
    # reset_num_timesteps=False: si el modelo fue cargado con pasos previos,
    # sigue contando desde ahi y entrena solo hasta llegar a total_timesteps
    # en total, en vez de sumarle total_timesteps nuevos arriba de los que ya tenia.
    model.learn(total_timesteps=config.total_timesteps, callback=callback, reset_num_timesteps=False)


def save_model(model: PPO, config: TrainingConfig) -> None:
    model.save(os.path.join(MODELS_DIR, config.model_name))


def train():
    config = TrainingConfig()
    env = build_env()
    model = build_model(env, config)
    checkpoint_callback = build_checkpoint_callback(config)
    try:
        train_model(model, config, checkpoint_callback)
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario, guardando el modelo antes de salir...")
    finally:
        save_model(model, config)
        env.close()


def main():
    train()


if __name__ == "__main__":
    main()
