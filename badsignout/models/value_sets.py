from enum import Enum

__all__=["SEX"]

class SEX(Enum):
    m = 'male'
    f = 'female'
    mtf = 'male-to-female'
    ftm = 'female-to-male'
    o = 'other'
