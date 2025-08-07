# experiments/exp1/train_independent_ppo.py

import os
from pettingzoo.mpe import simple_tag_v3
import supersuit as ss
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import  VecMonitor

def make_env():
    # 1) 環境生成
    env = simple_tag_v3.parallel_env(
        max_cycles=25, continuous_actions=False
    )
    # 2) 観測と行動空間をパディングして均一化
    env = ss.pad_observations_v0(env)
    env = ss.pad_action_space_v0(env)
    # 3) VecEnv に変換 (1つの env に対して 1つの VecEnv)
    vec_env = ss.pettingzoo_env_to_vec_env_v1(env)
    # 4) 必要なら複数コピーを concat（ここでは 1 つだけ）
    vec_env = ss.concat_vec_envs_v1(
        vec_env,
        num_vec_envs=1,
        base_class="stable_baselines3"
    )
    return vec_env

def main():
    log_dir = os.path.join(os.path.dirname(__file__), "../../logs/exp1/")
    os.makedirs(log_dir, exist_ok=True)

    # VecEnv を 1 インスタンス生成＆ログ記録
    env = VecMonitor(make_env(), log_dir)

    # PPO エージェント（MLP ポリシー）
    model = PPO(
        policy="MlpPolicy",
        env=env,
        verbose=1,
        tensorboard_log=log_dir
    )

    # 学習開始（ステップ数はお好みで調整）
    model.learn(total_timesteps=100_000)

    # モデル保存
    save_path = os.path.join(log_dir, "ppo_simple_tag")
    model.save(save_path)
    print(f"Model saved to {save_path}")

    env.close()

if __name__ == "__main__":
    main()
