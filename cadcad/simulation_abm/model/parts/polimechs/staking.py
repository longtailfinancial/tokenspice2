
def p_staking(params, substep, state_history, prev_state):
    """
    Staking on datasets.
    """
    agents = prev_state['agents']
    pool_agents = prev_state['pool_agents']
    state = prev_state['state']
    pools_staked = prev_state['total_staked']

    staker_agents = {k: v for k, v in agents.items() if 'Energy Web Staker' in v.name}
 
    agent_delta = {}

    for label, agent in list(staker_agents.items()):
        agent.takeStep(state, pools_staked, pool_agents)
        agent_delta[label] = agent

    return {'agent_delta': agent_delta,
            }

def s_staking(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta in list(policy_input['agent_delta'].items()):
        updated_agents[label] = delta
    return ('agents', updated_agents)

