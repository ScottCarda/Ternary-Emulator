from ..Exceptions import RegisterAssignmentError
from .FrozenDict import FrozenDict

'''
Conditions:
    
    AL  000:    Always
    EQ  001:    Equal ( S flag = 1 )
    CC  002:    Carry Clear ( C flag = 0 )
    MI  010:    Negative ( S flag = 0 )
    VC  011:    Overflow Clear ( V flag = 0 )
    LS  012:    Unsigned Lower ( C flag = 0, OR S flag = 1 )
    LT  020:    < ( IS_F(S flag) = IS_F(V flag) )    
    LE  021:    <= ( S flag = 1 OR IS_F(S flag) = IS_F(V flag) )
    
    GT  201:    > ( S flag = 1 AND IS_F(S flag) != IS_F(V flag) )
    GE  202:    >= ( IS_F(S flag) != IS_F(V flag) )
    HI  210:    Unsigned Higher ( C flag != 0 AND S flag != 1 )
    VS  211:    Overflow Set ( V flag != 0 )
    PL  212:    Positive ( S flag != 0 ) - maybe: ( S flag = 2 )
    CS  220:    Carry Set ( C flag != 0 )
    NE  221:    Not Equal ( S flag != 1 )
    NV  222:    Never
'''

def CPSR_Table():
    cpsr = CPSR()
    
    conditions = [cond for cond in cpsr.cond]
    conditions.sort()
    
    print( ( '|' + '*'*3 )*3 + '|' + ( '|' + '*'*3 )*16 + '|' )
    
    print( '| S | C | V ||', end = '' )
    print( ' AL|', end = '' )
    print( ' EQ|', end = '' )
    print( ' CC|', end = '' )
    print( ' MI|', end = '' )
    print( ' VC|', end = '' )
    print( ' LS|', end = '' )
    print( ' LT|', end = '' )
    print( ' LE|', end = '' )
    print( ' GT|', end = '' )
    print( ' GE|', end = '' )
    print( ' HI|', end = '' )
    print( ' VS|', end = '' )
    print( ' PL|', end = '' )
    print( ' CS|', end = '' )
    print( ' NE|', end = '' )
    print( ' NV|' )
    
    print( ( '|' + '*'*3 )*3 + '|' + ( '|' + '*'*3 )*16 + '|' )
    
    for s in range(3):
        cpsr.S = s
        for c in range(3):
            cpsr.C = c
            for v in range(3):
                cpsr.V = v
            
                print( '| ' + str(cpsr.S) + ' | ' + str(cpsr.C) + ' | ' + str(cpsr.V) + ' ||', end = '' )
                for condcode in conditions:
                    print( ' ' + ( 'X' if cpsr.cond[condcode]() else '-' ) + ' |', end = '' )
                print( '' )
    
    print( ( '|' + '*'*3 )*3 + '|' + ( '|' + '*'*3 )*16 + '|' )

class CPSR(object):
    
    from .Cond import   \
        AL as __AL,     \
        EQ as __EQ,     \
        CC as __CC,     \
        MI as __MI,     \
        VC as __VC,     \
        LS as __LS,     \
        LT as __LT,     \
        LE as __LE,     \
        GT as __GT,     \
        GE as __GE,     \
        HI as __HI,     \
        VS as __VS,     \
        PL as __PL,     \
        CS as __CS,     \
        NE as __NE,     \
        NV as __NV
    
    def __init__(self, S = 0, C = 0, V = 0):
        self.S = S
        self.C = C
        self.V = V
        
        self.cond = {
            '000':self.__AL,
            '001':self.__EQ,
            '002':self.__CC,
            '010':self.__MI,
            '011':self.__VC,
            '012':self.__LS,
            '020':self.__LT,
            '021':self.__LE,
            
            '201':self.__GT,
            '202':self.__GE,
            '210':self.__HI,
            '211':self.__VS,
            '212':self.__PL,
            '220':self.__CS,
            '221':self.__NE,
            '222':self.__NV
        }
        self.cond = FrozenDict(self.cond)

    def __str__(self):
        return "{0.S}{0.C}{0.V}".format( self )
        
    def __repr__(self):
        return "CPSR(S={0.S}, C={0.C}, V={0.V})".format( self )
        
    def clear(self):
        self.S = 0
        self.C = 0
        self.V = 0
        return
        
    @property
    def S(self):
        return self.__S
        
    @S.setter
    def S(self, val):
        if type(val) is int and 0 <= val <= 2:
            self.__S = val
        else:
            raise RegisterAssignmentError( val )
            
    @property
    def C(self):
        return self.__C
        
    @C.setter
    def C(self, val):
        if type(val) is int and 0 <= val <= 2:
            self.__C = val
        else:
            raise RegisterAssignmentError( val )
            
    @property
    def V(self):
        return self.__V
        
    @V.setter
    def V(self, val):
        if type(val) is int and 0 <= val <= 2:
            self.__V = val
        else:
            raise RegisterAssignmentError( val )
    
    #def cond(self, cond_str):
    #    return self.__cond[cond_str]()

