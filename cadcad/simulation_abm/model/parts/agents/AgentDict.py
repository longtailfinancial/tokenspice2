from enforce_typing import enforce_types # type: ignore[import]

from .PublisherAgent import PublisherAgent
from .PoolAgent import PoolAgent
from .StakerspeculatorAgent import StakerspeculatorAgent
from .DataconsumerAgent import DataconsumerAgent
from .EWPublisherAgent import EWPublisherAgent
from .EWOptimizerAgent import EWOptimizerAgent

@enforce_types
class AgentDict(dict):
    """Dict of Agent"""
    def __init__(self,*arg,**kw):
        """
        Extend the dict object to get the best of both worlds (object/dict)
        """
        super(AgentDict, self).__init__(*arg, **kw)

    def filterByNonzeroStake(self, agent):
        """Which pools has 'agent' staked on?"""
        return AgentDict({pool_agent.name : pool_agent
                          for pool_agent in self.filterToPool().values()
                          if agent.BPT(pool_agent.pool) > 0.0})
    
    def filterToPool(self):
        return self.filterByClass(PoolAgent)

    def filterToEWDevicePool(self):
        return self.filterByEWDeviceClass(PoolAgent)

    def filterToPublisher(self):
        return self.filterByClass(PublisherAgent)

    def filterToStakerspeculator(self):
        return self.filterByClass(StakerspeculatorAgent)

    def filterToDataconsumer(self):
        return self.filterByClass(DataconsumerAgent)
    
    def filterByClass(self, _class):
        return AgentDict({agent.name : agent
                          for agent in self.values()
                          if isinstance(agent, _class)})

    # DEC update Energyy Web

    def filterToEWPublisher(self):
        return self.filterByClass(EWPublisherAgent)

    def filterToEWOptimizer(self):
        return self.filterByClass(EWOptimizerAgent)

    def filterByEWDevicePool(self, _class):
        return AgentDict({agent.name : agent
                          for agent in self.values()
                          if isinstance(agent, _class) and 'Energy Web Device Pool' in agent.name})
    
