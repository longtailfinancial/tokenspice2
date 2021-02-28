import logging
from typing import Optional
log = logging.getLogger('marketagents')

from enforce_typing import enforce_types # type: ignore[import]
import random

from .EWBaseAgent import EWBaseAgent
from .EWPoolAgent import EWPoolAgent
from ..util import constants
from ..util.constants import POOL_WEIGHT_DT, POOL_WEIGHT_OCEAN
from ..web3engine import bfactory, bpool, datatoken, dtfactory, globaltokens
from ..web3tools.web3util import toBase18
        
from dataclasses import dataclass, field

@dataclass
class EWPublisherAgent(EWBaseAgent):
    # __slots__ = ['_s_since_create', '_s_between_create', '_s_since_unstake', '_s_between_unstake']
    _s_since_create: int = 0
    _s_between_create: int = 1 * constants.S_PER_DAY #magic number
    _s_since_unstake: int = 0
    _s_between_unstake: int = 8 * constants.S_PER_HOUR
    _s_since_stake: int = 0
    _s_between_stake: int = 6 * constants.S_PER_HOUR
        
    def takeStep(self, state, pool_agents) -> Optional[EWPoolAgent]:
        self._s_since_create += state.ss.time_step
        self._s_since_unstake += state.ss.time_step
        pool_agent = None

        if self._doCreatePool():
            self._s_since_create = 0
            pool_agent = self._createPoolAgent(pool_agents)

        if self._doUnstakeOCEAN(pool_agents):
            self._s_since_unstake = 0
            self._unstakeOCEANsomewhere(pool_agents)

        if self._doStakeOCEAN(pool_agents):
            self._s_since_stake = 0
            self._stakeOCEANsomewhere(pool_agents)


        return pool_agent

    def _doCreatePool(self) -> bool:
        if self.OCEAN < 200.0: #magic number
            return False
        return self._s_since_create >= self._s_between_create

    def _createPoolAgent(self, pool_agents) -> EWPoolAgent:        
        assert self.OCEAN > 0.0, "should not call if no OCEAN"
        wallet = self._wallet._web3wallet
        OCEAN = globaltokens.OCEANtoken()
        
        #name
        pool_i = len(pool_agents)
        dt_name = f'DT{pool_i}'
        # >>> DEC change
        pool_agent_name = f'ewpool{pool_i}'
        
        #new DT
        DT = self._createDatatoken(dt_name, mint_amt=1000.0) #magic number

        #new pool
        pool_address = bfactory.BFactory().newBPool(from_wallet=wallet)
        pool = bpool.BPool(pool_address)
        #bind tokens & add initial liquidity
        OCEAN_bind_amt = 0.3*self.OCEAN #magic number: use all the OCEAN
        DT_bind_amt = 20.0 #magic number
                
        DT.approve(pool.address, toBase18(DT_bind_amt), from_wallet=wallet)
        OCEAN.approve(pool.address, toBase18(OCEAN_bind_amt),from_wallet=wallet)
        
        pool.bind(DT.address, toBase18(DT_bind_amt),
                  toBase18(POOL_WEIGHT_DT), from_wallet=wallet)
        pool.bind(OCEAN.address, toBase18(OCEAN_bind_amt),
                  toBase18(POOL_WEIGHT_OCEAN), from_wallet=wallet)
        
        pool.finalize(from_wallet=wallet)

        #create agent
        pool_agent = EWPoolAgent(pool_agent_name, pool_address)
        
        # print(f'{self.name} balance now: {self.OCEAN} OCEAN')
        return pool_agent

    def _doUnstakeOCEAN(self, pool_agents) -> bool:
        i = 0
        for pool_agent in pool_agents:
            if self.BPT(bpool.BPool(pool_agent.pool_address)) > 0.0:
                i += 1
        if i == 0:
            return False
        return self._s_since_unstake >= self._s_between_unstake

    def _doStakeOCEAN(self, pool_agents) -> bool:
        i = 0
        for pool_agent in pool_agents:
            if self.BPT(bpool.BPool(pool_agent.pool_address)) > 0.0:
                i += 1
        if i == 0:
            return False
        return self._s_since_stake >= self._s_between_stake

    def _getBPT(self, pool_agents):
        BPT = 0.0
        pool_agent = None
        while BPT == 0.0:
            pool_agent = random.choice(list(pool_agents))
            BPT = self.BPT(bpool.BPool(pool_agent.pool_address))
        BPT_reserved = 0.10 * random.random() * BPT #magic number
        return pool_agent, BPT_reserved

    def _unstakeOCEANsomewhere(self, pool_agents):
        """Choose what pool to unstake and by how much. Then do the action."""
        pool_agent, BPT_reserved = self._getBPT(pool_agents)
        self.unstakeOCEAN(BPT_reserved, bpool.BPool(pool_agent.pool_address))
        print(f'{self.name} unstake from {pool_agent.name} : {BPT_reserved} BPT')

    def _stakeOCEANsomewhere(self, pool_agents):
        """Choose what pool to stake and by how much. Then do the action."""
        pool_agent, BPT_reserved = self._getBPT(pool_agents)
        self.unstakeOCEAN(BPT_reserved, bpool.BPool(pool_agent.pool_address))
        print(f'{self.name} stake on {pool_agent.name} : {BPT_reserved} BPT')

    def _createDatatoken(self,dt_name:str,mint_amt:float)-> datatoken.Datatoken:
        """Create datatoken contract and mint DTs to self."""
        wallet = self._wallet._web3wallet
        DT_address = dtfactory.DTFactory().createToken(
            '', dt_name, dt_name, toBase18(mint_amt), from_wallet=wallet)
        DT = datatoken.Datatoken(DT_address)
        DT.mint(wallet.address, toBase18(mint_amt), from_wallet=wallet)
        return DT
