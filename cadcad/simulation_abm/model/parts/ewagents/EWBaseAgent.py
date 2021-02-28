import logging
log = logging.getLogger('ewbaseagent')


from ..util.constants import SAFETY
from ..util.strutil import StrMixin
from .EWAgentWallet import EWAgentWallet
from ..web3engine import bpool, datatoken, globaltokens
from ..util.constants import SAFETY
from ..util.strutil import StrMixin
from ..web3tools.web3util import toBase18

from dataclasses import dataclass, field

@dataclass
class EWBaseAgent:
    # __slots__ = ['name', 'USD', 'OCEAN', 'private_key']
    name: str
    USD: float = 0.0
    OCEAN: float = 0.0
    private_key: str = None
    _wallet: EWAgentWallet = None

    """This can be a data buyer, publisher, etc. Sub-classes implement each."""
    def __post_init__(self):
        self._wallet = EWAgentWallet(self.USD, self.OCEAN, private_key=self.private_key)

    #=======================================================================
    #USD-related
    def USD(self) -> float:
        return self._wallet.USD() 
    
    def receiveUSD(self, amount: float) -> None:
        self._wallet.depositUSD(amount) 

    def _transferUSD(self, receiving_agent, amount: float) -> None:
        """set receiver to None to model spending, without modeling receiver"""
        if SAFETY:
            assert isinstance(receiving_agent, EWBaseAgent) or (receiving_agent is None)
        if receiving_agent is not None:
            self._wallet.transferUSD(receiving_agent._wallet, amount)
        else:
            self._wallet.withdrawUSD(amount)
        
    #=======================================================================
    #OCEAN-related
    def OCEAN(self) -> float:
        return self._wallet.OCEAN() 

    def receiveOCEAN(self, amount: float) -> None:
        self._wallet.depositOCEAN(amount)

    def _transferOCEAN(self, receiving_agent, amount: float) -> None:
        """set receiver to None to model spending, without modeling receiver"""
        if SAFETY:
            assert isinstance(receiving_agent, EWBaseAgent) or (receiving_agent is None)
        if receiving_agent is not None:
            self._wallet.transferOCEAN(receiving_agent._wallet, amount)
        else:
            self._wallet.withdrawOCEAN(amount)

    #=======================================================================
    #datatoken and pool-related
    def DT(self, dt:datatoken.Datatoken) -> float:
        return self._wallet.DT(dt)
    
    def BPT(self, pool:bpool.BPool) -> float:
        return self._wallet.BPT(pool)

    def stakeOCEAN(self, OCEAN_stake:float, pool:bpool.BPool):
        self._wallet.stakeOCEAN(OCEAN_stake, pool)

    def unstakeOCEAN(self, BPT_unstake:float, pool:bpool.BPool):
        self._wallet.unstakeOCEAN(BPT_unstake, pool)