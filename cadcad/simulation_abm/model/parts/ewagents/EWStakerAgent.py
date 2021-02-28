import logging
log = logging.getLogger('marketagents')
from typing import Optional

import random

from .EWBaseAgent import EWBaseAgent
from .EWPoolAgent import EWPoolAgent

from ..web3engine import bfactory, bpool, btoken, datatoken, dtfactory
from ..web3tools.web3util import toBase18
from ..util import constants
from operator import itemgetter
 
from dataclasses import dataclass, field

@dataclass
class EWStakerAgent(EWBaseAgent):
    """Speculates by staking and unstaking"""
    _s_since_speculate: int= 0
    _s_between_speculates: int = 4 * constants.S_PER_HOUR #magic number
        
    def takeStep(self, state, pools_staked, pool_agents):
        self._s_since_speculate += state.ss.time_step

        if self._doSpeculateAction(pools_staked):
            self._s_since_speculate = 0
            self._speculateAction(pools_staked, pool_agents)

    def _doSpeculateAction(self, pools_staked):
        if not pools_staked:
            return False
        else:
            return self._s_since_speculate >= self._s_between_speculates

    def _speculateAction(self, pools_staked, pool_agents):

        print(f'Pools staked: {pools_staked}')
        # get the Pools
        pool_to_stake, pool_to_unstake = self._selectPoolToStakeAndUnstake(pools_staked)
        unstake_pool = self._getPoolAgent(pool_agents, pool_to_unstake)
        stake_pool = self._getPoolAgent(pool_agents, pool_to_stake)
        # print(pool_agents)
        # print('Unstake pool: ', unstake_pool)
        BPT = 0.0
        if unstake_pool:
            BPT = self.BPT(bpool.BPool(unstake_pool.pool_address))
        print(f'BPT on unstake pool {pool_to_unstake} : {BPT}')

        # unstake bij 50% chance
        if unstake_pool and BPT > 0.0 and random.random() < 0.50: #magic number
            BPT_sell = 0.10 * random.random() * BPT #magic number
            self.unstakeOCEAN(BPT_sell, bpool.BPool(unstake_pool.pool_address))
            print(f'{self.name} unstake from {pool_to_unstake} : {BPT_sell} BPT')

        BPT = self.BPT(bpool.BPool(stake_pool.pool_address))
        print(f'BPT on stake pool {pool_to_stake} : {BPT}')
        # stake bij 50% chance
        if stake_pool and random.random() > 0.50: #magic number
            OCEAN_stake = 0.10 * random.random() * self.OCEAN #magic number
            self.stakeOCEAN(OCEAN_stake, bpool.BPool(stake_pool.pool_address))
            print(f'{self.name} stake on {pool_to_stake} : {OCEAN_stake} OCEAN')
        

    def _selectPoolToStakeAndUnstake(self, pools_staked):
        pools_sorted = sorted(pools_staked.items(), key=lambda x: x[1]['OCEAN'], reverse=True)
        return pools_sorted[-1][0], pools_sorted[0][0]
    
    def _getPoolAgent(self, pool_agents, name) -> Optional[EWPoolAgent]:
        for pool in pool_agents:
            if pool.name == name:
                return pool
        return None

