from dataclasses import make_dataclass
import logging
log = logging.getLogger('marketagents')

from enforce_typing import enforce_types # type: ignore[import]
import typing

from .EWBaseAgent import EWBaseAgent
from ..web3engine import bpool, btoken, datatoken, globaltokens
from ..web3tools.web3util import toBase18, fromBase
from dataclasses import dataclass, field

@dataclass
class EWPoolAgent(EWBaseAgent):
    # __slots__ = ['pool_address', '_dt_address']
    pool_address: str = ''
    _dt_address: str = ''

    def __init__(self, name: str, pool_address):
        super().__init__(name, USD=0.0, OCEAN=0.0)
        self.pool_address = pool_address
        self._dt_address = self._datatokenAddress()

    def takeStep(self):
        pass

    @property
    def pool(self) -> bpool.BPool:
        return bpool.BPool(self.pool_address)
    
    @property
    def datatoken_address(self) -> str:
        return self._dt_address
    
    @property
    def datatoken(self) -> datatoken.Datatoken:
        return datatoken.Datatoken(self._dt_address)
        
    def _datatokenAddress(self):
        pool = bpool.BPool(self.pool_address)
        addrs = pool.getCurrentTokens()
        assert len(addrs) == 2
        OCEAN_addr = globaltokens.OCEANtoken().address
        for addr in addrs:
            if addr != OCEAN_addr:
                return addr
        raise AssertionError("should never get here")

    # for Staker and Optimizer policies 
    def getBalances(self):
        pool = bpool.BPool(self.pool_address)
        addrs = pool.getCurrentTokens()
        assert len(addrs) == 2
        symbols = [btoken.BToken(addr).symbol()
                       for addr in addrs]
        balances = {}
        for addr, symbol in zip(addrs, symbols):
            balance_base = pool.getBalance_base(addr)
            dec = btoken.BToken(addr).decimals()
            balance = fromBase(balance_base, dec)
            balances[symbol] = balance
        return balances
    
    def getOceanBalance(self):
        balances = self.getBalances()
        return balances['OCEAN']