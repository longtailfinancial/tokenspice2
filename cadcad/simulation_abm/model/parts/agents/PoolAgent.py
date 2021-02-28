import logging
log = logging.getLogger('marketagents')

from enforce_typing import enforce_types # type: ignore[import]
import random

from .BaseAgent import BaseAgent
from ..web3engine import bpool, datatoken, globaltokens
from ..web3tools.web3util import toBase18
            
@enforce_types
class PoolAgent(BaseAgent):    
    def __init__(self, name: str, pool_address):
        super().__init__(name, USD=0.0, OCEAN=0.0)
        self.pool_address = pool_address
        
        self._dt_address = self._datatokenAddress()
        # self._dt = datatoken.Datatoken(self._dt_address)

    @property
    def pool(self) -> bpool.BPool:
        return bpool.BPool(self.pool_address)
    
    @property
    def datatoken_address(self) -> str:
        return self._dt_address
    
    @property
    def datatoken(self) -> datatoken.Datatoken:
        return datatoken.Datatoken(self._dt_address)
        
    def takeStep(self):
        #it's a smart contract robot, it doesn't initiate anything itself
        pass
        
    def _datatokenAddress(self):
        pool = bpool.BPool(self.pool_address)
        addrs = pool.getCurrentTokens()
        assert len(addrs) == 2
        OCEAN_addr = globaltokens.OCEANtoken().address
        for addr in addrs:
            if addr != OCEAN_addr:
                return addr
        raise AssertionError("should never get here")
