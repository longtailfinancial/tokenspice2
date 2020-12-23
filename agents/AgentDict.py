# import enforce

from agents.PublisherAgent import PublisherAgent
from agents.PoolAgent import PoolAgent
from agents.StakerspeculatorAgent import StakerspeculatorAgent
from agents.DataconsumerAgent import DataconsumerAgent

# @enforce.runtime_validation
class AgentDict(dict):
    """Dict of Agent"""
    
    def filterByNonzeroStake(self, agent):
        """Which pools has 'agent' staked on?"""
        return AgentDict({pool_agent.name : pool_agent
                          for pool_agent in self.filterToPool().values()
                          if agent.BPT(pool_agent.pool) > 0.0})
    
    def filterToPool(self):
        return self.filterByClass(PoolAgent)

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
    
