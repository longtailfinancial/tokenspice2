import random
from ..agents.DataconsumerAgent import DataconsumerAgent
from ..agents.AgentDict import AgentDict

def p_consume_datasets(params, substep, state_history, prev_state):
    """
    Consuming datasets.
    """
    step = prev_state['timestep']
    test = f'p_consume_datasets, {step} - {substep}'
    # print(test)
    agents = prev_state['agents']
    state = prev_state['state']

    dataconsumer_agents = {k: v for k, v in agents.items() if 'Dataconsumer' in v.name}
 
    agent_delta = {}

    for label, agent in list(dataconsumer_agents.items()):
        agent.takeStep(state)
        agent_delta[label] = agent

    return {'agent_delta': agent_delta,
            }

def s_consume_datasets(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta in list(policy_input['agent_delta'].items()):
        updated_agents[label] = delta
    return ('agents', updated_agents)


