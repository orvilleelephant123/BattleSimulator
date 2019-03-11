# import local objects

# import Unit and Army
from .unit import Unit
from .army import Army, DelayArmy
from .battle import Battle
from .simulator import simulate_battle
from .simplot import *
from .ai import *
from .imageplot import *

__version__ = "0.1.3"
__name__ = "battlesim"