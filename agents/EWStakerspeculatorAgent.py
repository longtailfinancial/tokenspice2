import logging
log = logging.getLogger('marketagents')

from enforce_typing import enforce_types # type: ignore[import]
import random

from agents.BaseAgent import BaseAgent
from web3engine import bfactory, bpool, btoken, datatoken, dtfactory
from web3tools.web3util import toBase18
from util import constants
                    
@enforce_types
class EWStakerspeculatorAgent(BaseAgent):
    """Speculates by staking and unstaking"""
    
    def __init__(self, name: str, USD: float, OCEAN: float):
        super().__init__(name, USD, OCEAN)

        self._s_since_speculate = 0
        self._s_between_speculates = 8 * constants.S_PER_HOUR #magic number
        
    def takeStep(self, state):
        self._s_since_speculate += state.ss.time_step

        if self._doSpeculateAction(state):
            self._s_since_speculate = 0
            self._speculateAction(state)

    def _doSpeculateAction(self, state):
        pool_agents = state.agents.filterToPool().values()
        if not pool_agents:
            return False
        else:
            return self._s_since_speculate >= self._s_between_speculates

    def _speculateAction(self, state):
        pool_agents = state.agents.filterToPool().values()
        assert pool_agents, "need pools to be able to speculate"
        
        # DEC update: optimizer agents
        optimizer_agents = state.agents.filterToOptimizer().values()
        assert optimizer_agents, "need Optimizers to be able to speculate"
        
        pool = random.choice(list(pool_agents)).pool
        optimizer = random.choice(list(optimizer_agents)).pool

        # DEC update: here's the place to put the staking logic according to the EWOptimizer agent performance.
        # The Staker should inspect the dataset of the EWOptimizer pool to correspond with the relating EWPublisher pool
        # if predictions are within certain bandwiths corresponding with the actual real metered data, Staker will stake
        # otherwise Staker will unstake
        # To Be Done....

        BPT = self.BPT(pool)
        
        if BPT > 0.0 and random.random() < 0.50: #magic number
            BPT_sell = 0.10 * BPT #magic number
            self.unstakeOCEAN(BPT_sell, pool)
            
        else:
            OCEAN_stake = 0.10 * self.OCEAN() #magic number
            self.stakeOCEAN(OCEAN_stake, pool)
        
            
