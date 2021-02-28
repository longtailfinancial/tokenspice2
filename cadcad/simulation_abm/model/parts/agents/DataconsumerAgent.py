import logging
log = logging.getLogger('marketagents')

from dataclasses import dataclass

@dataclass
class DataconsumerAgent:
    name: str
    USD: float
    OCEAN: float

    def takeStep(self, state):
        self.OCEAN -= 1
