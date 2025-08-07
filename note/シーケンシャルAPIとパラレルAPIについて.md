
・シーケンシャルAPI（AEC: Agent-Environment Cycle）とパラレルAPIについて
    ・主な違いはエージェントの観測・行動・環境ステップを【順番に1エージェントずつ】行うか，全エージェントを同時に」行うかという点らしい
         シーケンシャルAPIの場合は1ステップごとにどのエージェントが動くかが明示的である，順番が減額に管理されるため，ターン制や逐次決定問題に向いている．
        エージェント一つ一つを個別に順番に見ていくイメージ
        実装がやや複雑で，step()/reset()を呼ばないとagent_iter()がassertエラーになる．
        独自ループが必要だったりする．
            コード例）
            ``` python
            env.reset()
            for agent in env.agent_iter():
                obs, reward, terminated, truncated, info = env.last()
                action = policy(agent, obs)
                env.step(action)
            ```
        一方でパラレルAPIは環境を中心にモデルをみていると思うな．全エージェントを同時に管理する感じ．実装がシンプルで済む．OpenAI Gymライクなインターフェースで並列環境を前提としたアルゴリズムと相性がいいらしい，
        同期型シミュレーションに適している⇒これが一番大きな要素
            code)
            ``` python
            obs_dict = env.reset()
            done = {agent: False for agent in env.agents}
            while not all(done.values()):
                actions = {agent: policy(agent, obs_dict[agent]) for agent in env.agents}
                obs_dict, reward_dict, terminations, truncations, info_dict = env.step(actions)
                done = {a: terminations[a] or truncations[a] for a in env.agents}
            ```