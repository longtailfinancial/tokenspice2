import logging
from typing import Optional
log = logging.getLogger('marketagents')

from enforce_typing import enforce_types # type: ignore[import]
import random

from .EWPublisherAgent import EWPublisherAgent
from .EWPoolAgent import EWPoolAgent
from ..util import constants
from ..util.constants import POOL_WEIGHT_DT, POOL_WEIGHT_OCEAN
from ..web3engine import bfactory, bpool, datatoken, dtfactory, globaltokens
from ..web3tools.web3util import toBase18
        
from dataclasses import dataclass, field

@dataclass
class EWOptimizerAgent(EWPublisherAgent):
    _ew_device_pool_name: str = ''

    def takeStep(self, state, pool_agents) -> Optional[EWPoolAgent]:
        pool_agent = None

        if self._doCreatePool(state):
            pool_agent = self._createPoolAgent(pool_agents)
            pool_agent.name = self._ew_device_pool_name + '-optimizer'

        if self._doUnstakeOCEAN(pool_agents):
            self._s_since_unstake = 0
            self._unstakeOCEANsomewhere(pool_agents)
        
        return pool_agent

    def _doCreatePool(self, state) -> bool:
        if self.OCEAN < 200.0: #magic number
            return False
        self._ew_device_pool_name = self._selectEWDevicePool(state)
        if self._ew_device_pool_name is not None:
            return True
        else:
            return False

    def _selectEWDevicePool(self, state) -> Optional[str]:
        pools = state.kpis.total_staked
        ew_device_pool_names = [label for label in pools.keys() if '-optimizer' not in label]
        if len(ew_device_pool_names) > 0:
            return random.choice(ew_device_pool_names)
        else:
            return None


