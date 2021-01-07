import logging
log = logging.getLogger('baseagent')

from abc import ABC, abstractmethod
from enforce_typing import enforce_types # type: ignore[import]
import typing

from agents import AgentWallet
from web3engine import bpool, datatoken, globaltokens
from util.constants import SAFETY
from util.strutil import StrMixin
from web3tools.web3util import toBase18

@enforce_types
class BaseAgent(ABC, StrMixin):
    """This can be a data buyer, publisher, etc. Sub-classes implement each."""
       
    def __init__(self, name: str, USD: float, OCEAN: float, private_key: str=None):
        self.name = name
        self._wallet = AgentWallet.AgentWallet(USD, OCEAN, private_key=private_key)

        #postconditions
        if private_key == None:
            assert self.USD() == USD
            assert self.OCEAN() == OCEAN
        else:
            # TODO
            # This is kind of weak - we should test for sum of current and previous
            assert self.USD() >= USD
            assert self.OCEAN() >= OCEAN

    #=======================================================================
    @abstractmethod
    def takeStep(self, state): #this is where the Agent does *work*
        pass

    #=======================================================================
    #USD-related
    def USD(self) -> float:
        return self._wallet.USD() 
    
    def receiveUSD(self, amount: float) -> None:
        self._wallet.depositUSD(amount) 

    def _transferUSD(self, receiving_agent, amount: float) -> None:
        """set receiver to None to model spending, without modeling receiver"""
        if SAFETY:
            assert isinstance(receiving_agent, BaseAgent) or (receiving_agent is None)
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
            assert isinstance(receiving_agent, BaseAgent) or (receiving_agent is None)
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
                            
