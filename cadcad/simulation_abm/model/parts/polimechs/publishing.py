import random
from ..agents.AgentDict import AgentDict

def p_publish_datasets(params, substep, state_history, prev_state):
    """
    Publishing datasets.
    """
    step = prev_state['timestep']
    test = f'p_publish_datasets, {step} - {substep}'
    # print(test)
    agents = prev_state['agents']
    pool_agents = prev_state['pool_agents']
    state = prev_state['state']
    publisher_agents = {k: v for k, v in agents.items() if 'Energy Web Publisher' in v.name}
 
    agent_delta = {}
    pool_agent_delta = pool_agents

    for label, agent in list(publisher_agents.items()):
        pool_agent = agent.takeStep(state, pool_agents)
        if pool_agent is not None:
            print("Pool Agent created!")
            pool_agent_delta.append(pool_agent)
        agent_delta[label] = agent

    return {'agent_delta': agent_delta,
            'pool_agent_delta': pool_agent_delta
            }

def s_publish_datasets(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta in list(policy_input['agent_delta'].items()):
        updated_agents[label] = delta
    return ('agents', updated_agents)

def s_new_pool_agent(params, substep, state_history, prev_state, policy_input):
    return ('pool_agents', policy_input['pool_agent_delta'])

