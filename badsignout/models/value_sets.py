from enum import Enum

__all__=["SEX", "ACTION"]

class SEX(Enum):
    m = 'male'
    f = 'female'
    mtf = 'male-to-female'
    ftm = 'female-to-male'
    o = 'other'

class ACTION(Enum):
    f = 'follow-up'
    o = 'order'
    r = 'round on'
