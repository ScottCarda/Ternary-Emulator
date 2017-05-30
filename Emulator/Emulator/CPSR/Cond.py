from ..ALU.Gates import IS_F

'''
Conditions:
    
    AL:    Always
    EQ:    Equal ( S flag = 1 )
    CC:    Carry Clear ( C flag = 0 )
    MI:    Negative ( S flag = 0 )
    VC:    Overflow Clear ( V flag = 0 )
    LS:    Unsigned Lower ( C flag = 0, OR S flag = 1 )
    LT:    < ( IS_F(S flag) = IS_F(V flag) )    
    LE:    <= ( S flag = 1 OR IS_F(S flag) = IS_F(V flag) )
    
    GT:    > ( S flag = 1 AND IS_F(S flag) != IS_F(V flag) )
    GE:    >= ( IS_F(S flag) != IS_F(V flag) )
    HI:    Unsigned Higher ( C flag != 0 AND S flag != 1 )
    VS:    Overflow Set ( V flag != 0 )
    PL:    Positive ( S flag != 0 ) - maybe: ( S flag = 2 )
    CS:    Carry Set ( C flag != 0 )
    NE:    Not Equal ( S flag != 1 )
    NV:    Never
'''

def AL(self):
    return True
AL.name = 'AL'
    
def EQ(self):
    return self.S == 1
EQ.name = 'EQ'

def CC(self):
    return self.C == 0
CC.name = 'CC'
    
def MI(self):
    return self.S == 0
MI.name = 'MI'
    
def VC(self):
    return self.V == 0
VC.name = 'VC'
    
def LS(self):
    return self.C == 0 or self.S == 1
LS.name = 'LS'
        
def LT(self):
    return IS_F(self.S) == IS_F(self.V)
LT.name = 'LT'
        
def LE(self):
    return self.S == 1 or IS_F(self.S) == IS_F(self.V)
LE.name = 'LE'
        


def GT(self):
    return not LE(self)
GT.name = 'GT'
        
def GE(self):
    return not LT(self)
GE.name = 'GE'
        
def HI(self):
    return not LS(self)
HI.name = 'HI'
        
def VS(self):
    return not VC(self)
VS.name = 'VS'
        
def PL(self):
    return not MI(self)
PL.name = 'PL'
        
def CS(self):
    return not CC(self)
CS.name = 'CS'

def NE(self):
    return not EQ(self)
NE.name = 'NE'

def NV(self):
    return False
NV.name = 'NV'
    
    

