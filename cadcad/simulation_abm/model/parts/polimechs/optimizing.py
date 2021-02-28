import random
from ..agents.EWPublisherAgent import EWPublisherAgent
from ..agents.AgentDict import AgentDict

def p_optimizing(params, substep, state_history, prev_state):
    """
    Optimizing the forecasting data token pool.
    """
    step = prev_state['timestep']
    # print(f'p_optimizing, {step} - {substep}')
    agents = prev_state['agents']
    state = prev_state['state']
    optimizer_agents = {k: v for k, v in agents.items() if 'Energy Web Optimizer' in v.name}
 
    agent_delta = {}

    for label, agent in list(optimizer_agents.items()):
        pool_agent = agent.takeStep(state, agents)
        if pool_agent is not None:
            agent_delta[pool_agent.name] = pool_agent
        agent_delta[label] = agent

    return {'agent_delta': agent_delta,
            }

def s_optimizing(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta in list(policy_input['agent_delta'].items()):
        updated_agents[label] = delta
    return ('agents', updated_agents)


