from ..agents.GrantTakingAgent import GrantTakingAgent
from ..agents.GrantGivingAgent import GrantGivingAgent
from ..agents import MinterAgents
from ..agents.OCEANBurnerAgent import OCEANBurnerAgent
from ..agents.RouterAgent import RouterAgent
import random

from ..agents.AgentDict import AgentDict

def p_logistics(params, substep, state_history, prev_state):
    """
    Do the logistics.
    """
    step = prev_state['timestep']
    # print(f'p_logistics, {step}:{substep}')

    agents = prev_state['agents']
    state = prev_state['state']
    pool_agents = prev_state['pool_agents']
    router_agents = AgentDict(agents).filterByClass(RouterAgent)
    ocean_burner_agents = AgentDict(agents).filterByClass(OCEANBurnerAgent)
    minter_agents = AgentDict(agents).filterByClass(MinterAgents.OCEANFuncMinterAgent)
    grantgiving_agents = AgentDict(agents).filterByClass(GrantGivingAgent)
    granttaking_agents = AgentDict(agents).filterByClass(GrantTakingAgent)
    
    agent_delta = {}

    for label, agent in list(router_agents.items()):
        agent.takeStep(state, agents)
        agent_delta[label] = agent

    for label, agent in list(ocean_burner_agents.items()):
        agent.takeStep(state)
        agent_delta[label] = agent

    for label, agent in list(minter_agents.items()):
        agent.takeStep(state, agents)
        agent_delta[label] = agent

    for label, agent in list(grantgiving_agents.items()):
        agent.takeStep(state, agents)
        agent_delta[label] = agent

    for label, agent in list(granttaking_agents.items()):
        agent.takeStep(state)
        agent_delta[label] = agent

    for agent in pool_agents:
        agent.takeStep()

    return {'agent_delta': agent_delta }

def s_logistics(params, substep, state_history, prev_state, policy_input):
    updated_agents = prev_state['agents'].copy()
    for label, delta in list(policy_input['agent_delta'].items()):
        updated_agents[label] = delta
    return ('agents', updated_agents)


