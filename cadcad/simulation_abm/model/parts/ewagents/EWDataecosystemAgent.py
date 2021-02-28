import logging
log = logging.getLogger('marketagents')

from enforce_typing import enforce_types # type: ignore[import]
import random
import names

from .EWBaseAgent import BaseAgent
from .EWPublisherAgent import EWPublisherAgent
from .EWStakerAgent import EWStakerAgent

from .DataconsumerAgent import DataconsumerAgent
from ..web3tools.web3util import toBase18
                    
from dataclasses import dataclass, field

@dataclass
class DataecosystemAgent(BaseAgent):
    """Will operate as a high-fidelity replacement for MarketplacesAgents,
    when it's ready."""     
        
    def takeStep(self, state):
            
        if self._doCreateEWStakerAgent(state):
            self._createEWStakerAgent(state)
            
        if self._doCreateDataconsumerAgent(state):
            self._createDataconsumerAgent(state)

        if self._doCreateEWPublisherAgent(state):
            self._createEWPublisherAgent(state)

        # if self._doCreateEWOptimizerAgent(state):
        #     self._createEWOptimizerAgent(state)


    def _doCreateEWPublisherAgent(self, state) -> bool:
        #magic number: rule - only create if no agents so far
        return (not state.publisherAgents()) 
            
    def _createPublisherAgent(self, state) -> PublisherAgent:
        name = "Publisher " + names.get_first_name()
        USD = 0.0 #FIXME magic number
        OCEAN = 1000.0 #FIXME magic number
        new_agent = PublisherAgent(name=name, USD=USD, OCEAN=OCEAN)
        state.addAgent(new_agent)

    def _doCreateStakerAgent(self, state) -> bool:
        #magic number: rule - only create if no agents so far
        return (not state.stakerspeculatorAgents())  
            
    def _createStakerspeculatorAgent(self, state) -> StakerspeculatorAgent:
        name = "Staker " + names.get_first_name()
        USD = 0.0 #FIXME magic number
        OCEAN = 1000.0 #FIXME magic number
        new_agent = StakerspeculatorAgent(name=name, USD=USD, OCEAN=OCEAN)
        state.addAgent(new_agent)

    def _doCreateDataconsumerAgent(self, state) -> bool:
        #magic number: rule - only create if no agents so far
        return (not state.dataconsumerAgents()) 
            
    def _createDataconsumerAgent(self, state) -> DataconsumerAgent:
        name = "Dataconsumer " + names.get_first_name()
        USD = 0.0 #FIXME magic number
        OCEAN = 1000.0 #FIXME magic number
        new_agent = DataconsumerAgent(name=name, USD=USD, OCEAN=OCEAN)
        state.addAgent(new_agent)

    def _doCreateEWPublisherAgent(self, state) -> bool:
        #magic number: rule - only create if no agents so far
        return (not state.ewpublisherAgents()) 
            
    def _createEWPublisherAgent(self, state) -> EWPublisherAgent:
        name = "Energy Web Publisher " + names.get_first_name()
        USD = 0.0 #FIXME magic number
        OCEAN = 2000.0 #FIXME magic number
        new_agent = EWPublisherAgent(name=name, USD=USD, OCEAN=OCEAN)
        state.addAgent(new_agent)

    def _doCreateEWOptimizerAgent(self, state) -> bool:
        #magic number: rule - only create if no agents so far
        return (not state.ewoptimizerAgents()) 
            
    def _createEWOptimizerAgent(self, state) -> EWPublisherAgent:
        name = "Energy Web Optimizer " + names.get_first_name()
        USD = 0.0 #FIXME magic number
        OCEAN = 2000.0 #FIXME magic number
        new_agent = EWOptimizerAgent(name=name, USD=USD, OCEAN=OCEAN)
        state.addAgent(new_agent)
