import logging
from typing import Optional
log = logging.getLogger('marketagents')

from enforce_typing import enforce_types # type: ignore[import]
import random

from . import AgentDict
from .BaseAgent import BaseAgent
from .PoolAgent import PoolAgent
from ..util import constants
from ..util.constants import POOL_WEIGHT_DT, POOL_WEIGHT_OCEAN
from ..web3engine import bfactory, bpool, datatoken, dtfactory, globaltokens
from ..web3tools.web3util import toBase18
        
@enforce_types
class EWPublisherAgent(BaseAgent):
    def __init__(self, name: str, USD: float, OCEAN: float):
        super().__init__(name, USD, OCEAN)
        
        self._s_since_create = 0
        self._s_between_create = 7 * constants.S_PER_DAY #magic number
        
        self._s_since_unstake = 0
        self._s_between_unstake = 3 * constants.S_PER_DAY #magic number
        
    def takeStep(self, state, pool_agents) -> Optional[PoolAgent]:
        self._s_since_create += state.ss.time_step
        self._s_since_unstake += state.ss.time_step
        pool_agent = None

        if self._doCreatePool():
            self._s_since_create = 0
            pool_agent = self._createPoolAgent(pool_agents)

        if self._doUnstakeOCEAN(pool_agents):
            self._s_since_unstake = 0
            self._unstakeOCEANsomewhere(pool_agents)
        
        return pool_agent

    def _doCreatePool(self) -> bool:
        if self.OCEAN() < 200.0: #magic number
            return False
        return self._s_since_create >= self._s_between_create

    def _createPoolAgent(self, pool_agents) -> PoolAgent:        
        assert self.OCEAN() > 0.0, "should not call if no OCEAN"
        wallet = self._wallet._web3wallet
        OCEAN = globaltokens.OCEANtoken()
        
        #name
        pool_i = len(pool_agents)
        dt_name = f'DT{pool_i}'
        # >>> DEC change
        pool_agent_name = f'pool{pool_i}'
        
        #new DT
        DT = self._createDatatoken(dt_name, mint_amt=1000.0) #magic number

        #new pool
        pool_address = bfactory.BFactory().newBPool(from_wallet=wallet)
        pool = bpool.BPool(pool_address)
        #bind tokens & add initial liquidity
        OCEAN_bind_amt = 0.5*self.OCEAN() #magic number: use all the OCEAN
        DT_bind_amt = 20.0 #magic number
                
        DT.approve(pool.address, toBase18(DT_bind_amt), from_wallet=wallet)
        OCEAN.approve(pool.address, toBase18(OCEAN_bind_amt),from_wallet=wallet)
        
        pool.bind(DT.address, toBase18(DT_bind_amt),
                  toBase18(POOL_WEIGHT_DT), from_wallet=wallet)
        pool.bind(OCEAN.address, toBase18(OCEAN_bind_amt),
                  toBase18(POOL_WEIGHT_OCEAN), from_wallet=wallet)
        
        pool.finalize(from_wallet=wallet)

        #create agent
        pool_agent = PoolAgent(pool_agent_name, pool_address)
        print("Pool created...")
        return pool_agent

    def _doUnstakeOCEAN(self, pool_agents) -> bool:
        i = 0
        for pool_agent in pool_agents:
            if self.BPT(bpool.BPool(pool_agent.pool_address)) > 0.0:
                i += 1
        if i == 0:
            return False
        return self._s_since_unstake >= self._s_between_unstake

    def _unstakeOCEANsomewhere(self, pool_agents):
        """Choose what pool to unstake and by how much. Then do the action."""
        pool_agent = random.choice(list(pool_agents))
        BPT = self.BPT(bpool.BPool(pool_agent.pool_address))
        BPT_unstake = 0.10 * BPT #magic number
        self.unstakeOCEAN(BPT_unstake, bpool.BPool(pool_agent.pool_address))

    def _createDatatoken(self,dt_name:str,mint_amt:float)-> datatoken.Datatoken:
        """Create datatoken contract and mint DTs to self."""
        wallet = self._wallet._web3wallet
        DT_address = dtfactory.DTFactory().createToken(
            '', dt_name, dt_name, toBase18(mint_amt), from_wallet=wallet)
        DT = datatoken.Datatoken(DT_address)
        DT.mint(wallet.address, toBase18(mint_amt), from_wallet=wallet)
        return DT
