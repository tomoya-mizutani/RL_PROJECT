# src/envs/test_pettingzoo.py

from pettingzoo.mpe import simple_tag_v3
import numpy as np

def run_one_episode():
    # パラレル環境を生成
    env = simple_tag_v3.parallel_env(max_cycles=25, continuous_actions=False)
    # reset() は obs_dict, info を返します
    obs_dict, info = env.reset()
    print("Agents:", env.agents)

    # 各エージェントが全員 done になるまでループ
    done = {agent: False for agent in env.agents}
    step = 0
    while not all(done.values()):
        # ランダムポリシー
        actions = {agent: env.action_space(agent).sample() for agent in env.agents}
        obs_dict, reward_dict, terminations, truncations, infos = env.step(actions)
        # terminated OR truncated を done とみなす
        done = {
            agent: terminations.get(agent, False) or truncations.get(agent, False)
            for agent in env.agents
        }
        # ログ出力
        for agent in env.agents:
            print(
                f"{agent}: obs={np.round(obs_dict[agent],2)}, "
                f"reward={reward_dict[agent]:.2f}, done={done[agent]}"
            )
        step += 1

    env.close()
    print(f"Episode finished in {step} steps")

if __name__ == "__main__":
    run_one_episode()
