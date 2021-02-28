from ..agents.MarketplacesAgent import MarketplacesAgent
from ..ewagents.EWPoolAgent import EWPoolAgent

import random

from ..agents.AgentDict import AgentDict
from ..agents.SimAgent import SimAgent

def p_accounting(params, substep, state_history, prev_state):
    """
    Update the state and KPIs.
    """
    step = prev_state['timestep']
    # print(f'p_accounting, {step} - {substep}')

    state = prev_state['state']
    agents = prev_state['agents']
    # EW update
    pool_agents = prev_state['pool_agents']
    total_staked = {}
    for pool_agent in pool_agents:
        total_staked[pool_agent.name] = pool_agent.getBalances()
    # mutant of SimEngine, logging
    sim_agents = AgentDict(agents).filterByClass(SimAgent)
    for label, agent in list(sim_agents.items()):
        agent.takeStep(state, agents, total_staked)

    marketplaces_agents = AgentDict(agents).filterByClass(MarketplacesAgent)
    for label, agent in list(marketplaces_agents.items()):
        agent.takeStep(state, agents)

    state.takeStep(agents)
    # print(f'State: {global_state.OCEANprice()}')
    state_delta = state

    return {'state_delta': state_delta,
            'total_staked': total_staked }

def s_accounting(params, substep, state_history, prev_state, policy_input):
    updated_stats = policy_input['state_delta']
    return ('state', updated_stats)

def s_staked(params, substep, state_history, prev_state, policy_input):
    updated_total_staked = policy_input['total_staked']
    return ('total_staked', updated_total_staked)
