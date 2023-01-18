import enum


@enum.unique
class SQLOperators(enum.Enum):
    '''Операции сравнения SQL'''
    EQ = 'equal'
    NE = 'not equal'
    GT = 'greater than'
    LT = 'less than'
    IN = 'in list'
