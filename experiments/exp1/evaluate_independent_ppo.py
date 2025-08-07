# experiments/exp1/evaluate_independent_ppo.py

import os
import numpy as np
from pettingzoo.mpe import simple_tag_v3
from pettingzoo.utils.conversions import aec_to_parallel
import supersuit as ss
from stable_baselines3 import PPO

def make_env():
    # 1) AEC 環境を生成
    env = simple_tag_v3.env(max_cycles=25, continuous_actions=False)
    # 2) 空間をパディング
    env = ss.pad_observations_v0(env)
    env = ss.pad_action_space_v0(env)
    # 3) AEC → Parallel API に変換
    env = aec_to_parallel(env)
    # 4) VecEnv 化 (v1) + 単一インスタンス連結
    vec_env = ss.pettingzoo_env_to_vec_env_v1(env)
    vec_env = ss.concat_vec_envs_v1(
        vec_env,
        num_vec_envs=1,
        base_class="stable_baselines3"
    )
    return vec_env

def evaluate_model(model_path: str, n_episodes: int = 20):
    # モデル読み込み
    model = PPO.load(model_path)
    # VecEnv を生成
    env = make_env()
    all_totals = []

    for ep in range(1, n_episodes + 1):
        obs_batch = env.reset()
        # 終了フラグの初期化
        dones = np.array([False] * env.num_envs)
        total_reward = 0.0

        # 1 エピソード分ループ
        while not all(dones):
            actions, _ = model.predict(obs_batch, deterministic=True)
            obs_batch, rewards, dones, infos = env.step(actions)
            # VecEnv の rewards は各 env の合計報酬
            total_reward += rewards[0]

        print(f"Episode {ep:02d}: total_reward = {total_reward:.2f}")
        all_totals.append(total_reward)

    env.close()
    arr = np.array(all_totals)
    print(f"\nAverage Reward over {n_episodes} episodes: {arr.mean():.2f} ± {arr.std():.2f}")

if __name__ == "__main__":
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../logs/exp1/ppo_simple_tag")
    evaluate_model(MODEL_PATH, n_episodes=20)
