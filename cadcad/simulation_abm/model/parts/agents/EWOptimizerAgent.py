import logging
from typing import Optional
log = logging.getLogger('marketagents')

from enforce_typing import enforce_types # type: ignore[import]
import random

from .BaseAgent import BaseAgent
from .PoolAgent import PoolAgent
from ..util import constants
from ..util.constants import POOL_WEIGHT_DT, POOL_WEIGHT_OCEAN
from ..web3engine import bfactory, bpool, datatoken, dtfactory, globaltokens
from ..web3tools.web3util import toBase18
        
@enforce_types
class EWOptimizerAgent(BaseAgent):    
    def __init__(self, name: str, USD: float, OCEAN: float):
        super().__init__(name, USD, OCEAN)
        
        self._s_since_create = 0
        self._s_between_create = 7 * constants.S_PER_DAY #magic number
        
        self._s_since_unstake = 0
        self._s_between_unstake = 3 * constants.S_PER_DAY #magic number

        self._device_pool = ""
        
    def takeStep(self, agents, step) -> Optional[PoolAgent]:
        self._s_since_create += step
        self._s_since_unstake += step
        pool_agent = None

        if self._doCreatePool():
            self._s_since_create = 0
            if self._checkIfDevicePool:
                pool_agent = self._createPoolAgent(agents)

        if self._doUnstakeOCEAN(agents):
            self._s_since_unstake = 0
            self._unstakeOCEANsomewhere(agents)

        return pool_agent

    def _doCreatePool(self) -> bool:
        if self.OCEAN() < 200.0: #magic number
            return False
        return self._s_since_create >= self._s_between_create

    def _checkIfDevicePool(self, agents) -> bool:
        if self._device_pool != "":
            return False
        device_pool_agents = agents.filterToEWDevicePool()
        if len(device_pool_agents) > 0:
            device_pool = random.choice()
            self._device_pool = device_pool.name
            return True
        else:
            return False

    def _createPoolAgent(self,agents) -> PoolAgent:        
        assert self.OCEAN() > 0.0, "should not call if no OCEAN"
        wallet = self._wallet._web3wallet
        OCEAN = globaltokens.OCEANtoken()
        
        #name
        pool_i = len(agents.filterToPool())
        dt_name = f'DT{pool_i}'
        # >>> DEC change
        
        pool_agent_name = f'Energy Web Forecast Pool {pool_i}'
        
        #new DT
        DT = self._createDatatoken(dt_name, mint_amt=1000.0) #magic number

        #new pool
        pool_address = bfactory.BFactory().newBPool(from_wallet=wallet)
        pool = bpool.BPool(pool_address)
        print("Pool create...")
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
        pool_agent = PoolAgent(pool_agent_name, pool)
        return pool_agent

    def _doUnstakeOCEAN(self, agents) -> bool:
        if not agents.filterByNonzeroStake(self):
            return False
        return self._s_since_unstake >= self._s_between_unstake

    def _unstakeOCEANsomewhere(self, agents):
        """Choose what pool to unstake and by how much. Then do the action."""
        pool_agents = agents.filterByNonzeroStake(self)
        pool_agent = random.choice(list(pool_agents.values()))
        BPT = self.BPT(pool_agent.pool)
        BPT_unstake = 0.10 * BPT #magic number
        self.unstakeOCEAN(BPT_unstake, pool_agent.pool)

    def _createDatatoken(self,dt_name:str,mint_amt:float)-> datatoken.Datatoken:
        """Create datatoken contract and mint DTs to self."""
        wallet = self._wallet._web3wallet
        DT_address = dtfactory.DTFactory().createToken(
            '', dt_name, dt_name, toBase18(mint_amt), from_wallet=wallet)
        DT = datatoken.Datatoken(DT_address)
        DT.mint(wallet.address, toBase18(mint_amt), from_wallet=wallet)
        return DT
