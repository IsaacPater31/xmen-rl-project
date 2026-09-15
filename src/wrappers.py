import gymnasium as gym


class MaxProgressRewardWrapper(gym.Wrapper):
    """Adds a bonus for reaching a new farthest position in the level.

    Backtracking (retreating to fight better) costs nothing since it never
    lowers the recorded max, but jittering back and forth can't be farmed
    for reward either - only genuinely new progress pays out.
    """

    def __init__(self, env, progress_key="pos_x", coefficient=0.1):
        super().__init__(env)
        self.progress_key = progress_key
        self.coefficient = coefficient
        self._max_progress = 0

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self._max_progress = info.get(self.progress_key, 0)
        return obs, info

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        progress = info.get(self.progress_key, self._max_progress)
        if progress > self._max_progress:
            reward += self.coefficient * (progress - self._max_progress)
            self._max_progress = progress
        return obs, reward, terminated, truncated, info
