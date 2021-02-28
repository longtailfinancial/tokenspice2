"""
Model logic structure.
"""

from .parts.polimechs.consuming import *
from .parts.polimechs.publishing import *
from .parts.polimechs.optimizing import *
from .parts.polimechs.accounting import *
from .parts.polimechs.logistics import *
from .parts.polimechs.staking import *


partial_state_update_block = [
    {
        'policies': {
            'logistics': p_logistics,
            'accounting': p_accounting,
        },
        'variables': {
            'agents': s_logistics,
            'state': s_accounting,
            'total_staked': s_staked
        }
    },
    {
        'policies': {
            'consume_datasets': p_consume_datasets,
        },
        'variables': {
            'agents': s_consume_datasets,
        }
    },
    {
        'policies': {
            'publish_datasets': p_publish_datasets,
        },
        'variables': {
            'agents': s_publish_datasets,
            'pool_agents': s_new_pool_agent,
        }
    },
    {
        'policies': {
            'publish_datasets': p_staking,
        },
        'variables': {
            'agents': s_staking,
        }
    },
    # {
    #     'policies': {
    #         'optimize': p_optimizing,
    #     },
    #     'variables': {
    #         'agents': s_optimizing,
    #     }
    # },


]
