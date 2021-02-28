"""
Simulation parameters.
"""

from .model.parts.util.constants import S_PER_DAY, S_PER_HOUR, S_PER_YEAR

MAX_DAYS = 5
SIMULATION_TIME_STEPS = int(MAX_DAYS * S_PER_DAY/S_PER_HOUR + 2)
