"""
Model initial state.
"""

# Dependencies

import random
import uuid
import logging
log = logging.getLogger('simstate')

from enforce_typing import enforce_types # type: ignore[import]
from typing import Set

from .parts.agents import MinterAgents
from .parts.agents.BaseAgent import BaseAgent
from .parts.agents.AgentDict import AgentDict
from .parts.agents.GrantGivingAgent import GrantGivingAgent
from .parts.agents.GrantTakingAgent import GrantTakingAgent
from .parts.agents.MarketplacesAgent import MarketplacesAgent
from .parts.agents.DataecosystemAgent import DataecosystemAgent
from .parts.agents.DataconsumerAgent import DataconsumerAgent

from .parts.agents.OCEANBurnerAgent import OCEANBurnerAgent
from .parts.agents.StakerspeculatorAgent import StakerspeculatorAgent
from .parts.agents.PoolAgent import PoolAgent



from .parts.agents.RouterAgent import RouterAgent
from .parts.ewagents.EWPublisherAgent import EWPublisherAgent
from .parts.ewagents.EWStakerAgent import EWStakerAgent
from .parts.ewagents.EWSimAgent import EWSimAgent

# from .parts.agents.EWOptimizerAgent import EWOptimizerAgent

from .SimStrategy import SimStrategy
from .SimState import SimState, funcOne
from .parts.util import mathutil, valuation
from .parts.util.mathutil import Range
from .parts.util.constants import *

import numpy as np
import names
from typing import Tuple, List, Dict
from itertools import cycle
from enum import Enum

MAX_DAYS = 3660
OUTPUT_DIR = 'output_test'

## yet to be implemented
agent_probabilities = [0.7,0.75,0.8,0.85,0.9,0.95]

ss = SimStrategy()
ss.setMaxTicks(MAX_DAYS * S_PER_DAY / ss.time_step + 1)
    
assert hasattr(ss, 'save_interval')
ss.save_interval = S_PER_DAY
simState = SimState(ss)

# init agents
# initial_agents = AgentDict()
initial_agents = {}


#Instantiate and connnect agent instances. "Wire up the circuit"
new_agents = list()

new_agents.append(EWSimAgent(
    name = "sim_logger", output_dir = OUTPUT_DIR
))

#FIXME: replace MarketplacesAgent with DataecosystemAgent, when ready
new_agents.append(MarketplacesAgent(
    name = "marketplaces1", USD=0.0, OCEAN=0.0,
    toll_agent_name = "opc_address",
    n_marketplaces = float(ss.init_n_marketplaces),
    revenue_per_marketplace_per_s = 2e3 / S_PER_MONTH, #magic number
    time_step = ss.time_step,
    ))

new_agents.append(DataconsumerAgent("Dataconsumer", 0.0, 1000.0))

new_agents.append(EWPublisherAgent(
    name="Energy Web Publisher " + names.get_first_name(), USD=0.0, OCEAN=400.0
))

new_agents.append(EWStakerAgent(
    name="Energy Web Staker " + names.get_first_name(), USD=0.0, OCEAN=500.0
))

new_agents.append(EWPublisherAgent(
    name="Energy Web Publisher " + names.get_first_name(), USD=0.0, OCEAN=400.0
))

new_agents.append(EWStakerAgent(
    name="Energy Web Staker " + names.get_first_name(), USD=0.0, OCEAN=500.0
))
# new_agents.append(EWOptimizerAgent(
#     name="Energy Web Optimizer " + names.get_first_name(), USD=0.0, OCEAN=1000.0
# ))

# new_agents.append(DataecosystemAgent(
#     name = "dataecosystem1", USD=0.0, OCEAN=0.0
# ))

new_agents.append(RouterAgent(
    name = "opc_address", USD=0.0, OCEAN=0.0,
    receiving_agents = {"ocean_dao" : simState.percentToOceanDao,
                        "opc_burner" : simState.percentToBurn}))

new_agents.append(OCEANBurnerAgent(
    name = "opc_burner", USD=0.0, OCEAN=0.0))

# #func = MinterAgents.ExpFunc(H=4.0)
func = MinterAgents.RampedExpFunc(H=4.0,                                 #magic number
                                    T0=0.5, T1=1.0, T2=1.4, T3=3.0,        #""
                                    M1=0.10, M2=0.25, M3=0.50)             #""
new_agents.append(MinterAgents.OCEANFuncMinterAgent(
    name = "ocean_51",
    receiving_agent_name = "ocean_dao",
    total_OCEAN_to_mint = UNMINTED_OCEAN_SUPPLY,
    s_between_mints = S_PER_DAY,
    func = func))

new_agents.append(GrantGivingAgent(
    name = "opf_treasury_for_ocean_dao",
    USD = 0.0, OCEAN = OPF_TREASURY_OCEAN_FOR_OCEAN_DAO,                 #magic number
    receiving_agent_name = "ocean_dao",
    s_between_grants = S_PER_MONTH, n_actions = 12 * 3))                 #""

new_agents.append(GrantGivingAgent(
    name = "opf_treasury_for_opf_mgmt",
    USD = OPF_TREASURY_USD, OCEAN = OPF_TREASURY_OCEAN_FOR_OPF_MGMT,     #magic number
    receiving_agent_name = "opf_mgmt",
    s_between_grants = S_PER_MONTH, n_actions = 12 * 3))                 #""

new_agents.append(GrantGivingAgent(
    name = "bdb_treasury",
    USD = BDB_TREASURY_USD, OCEAN = BDB_TREASURY_OCEAN,                  #magic number
    receiving_agent_name = "bdb_mgmt",
    s_between_grants = S_PER_MONTH, n_actions = 17))                     #""

new_agents.append(RouterAgent(
    name = "ocean_dao",
    receiving_agents = {"opc_workers" : funcOne},
    USD=0.0, OCEAN=0.0))

new_agents.append(RouterAgent(
    name = "opf_mgmt",
    receiving_agents = {"opc_workers" : funcOne},
    USD=0.0, OCEAN=0.0))
                
new_agents.append(RouterAgent(
    name = "bdb_mgmt",
    receiving_agents = {"bdb_workers" : funcOne},
    USD=0.0, OCEAN=0.0))

new_agents.append(GrantTakingAgent(
    name = "opc_workers", USD=0.0, OCEAN=0.0))

new_agents.append(GrantTakingAgent(
    name = "bdb_workers", USD=0.0, OCEAN=0.0))


for agent in new_agents:
    initial_agents[agent.name] = agent
    print(agent)

from collections import defaultdict

# initial_states = {
#     'granttakers_revenue': 0.0,
#     'revenue_per_marketplace': defaultdict(lambda: 0.0), 
#     'total_OCEAN_staked': defaultdict(lambda: 0.0), 
#     'n_marketplaces': 1,
#     'marketplace_percent_toll_to_ocean': 0.0,
#     'total_OCEAN_minted': 0.0,
#     'total_OCEAN_burned': 0.0,
#     'total_OCEAN_minted_USD': 0.0,
#     'total_OCEAN_burned_USD': 0.0,
# }

genesis_states = {
    'agents': initial_agents,
    'pool_agents': [],
    'state': simState,
    'total_staked': defaultdict(lambda: 0.0), 
}
