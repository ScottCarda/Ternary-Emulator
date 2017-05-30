from .. import ALU
from ..Addressing import normal_AMs, scale_AMs, mem_AMs
from ..Exceptions import HaltingException as HaltExcept, OpNotImplementedException as NoImpl
from ..Register import Register

'''
Opcodes:

    000: HALT
    001: NO_OP
    002: CLEAR
    
    010: LOAD
    011: STORE
    012: EXCHANGE
    
    020: ADD
    021: SUB
    022: MOVE
    
    100: AND
    101: OR
    102: XOR
   
    110: F_NOT
    111: N_NOT
    112: T_NOT
   
    120: ISF
    121: ISN
    122: IST
   
    200: LSR
    201: ASR
    202: LSL
   
    210: SHIFT_M
    211: SHIFT_P
    212: <bad>
   
    220: JUMP
    221: <bad>
    222: <bad>

'''

class Operation(object):
    def __init__( self, func, name, num_args, AMs = normal_AMs, always_exec = False, is_jump = False, opr2_update = False ):
        self.__func = func
        self.name = name
        self.num_args = num_args
        self.AMs = AMs
        self.always_exec = always_exec
        self.is_jump = is_jump
        self.opr2_update = opr2_update
        
    def __call__( self, CPSR, DEST, OPR1, OPR2, RAM ):
        return self.__func( CPSR, DEST, OPR1, OPR2, RAM )
     
def makeOperation( name, num_args, AMs = normal_AMs, always_exec = False, is_jump = False, opr2_update = False ):
    def temp( func ):

        wrapper = Operation( func, name, num_args, AMs, always_exec, is_jump, opr2_update )
        
        return wrapper
    return temp

@makeOperation( 'HALT ', 0, AMs = normal_AMs | mem_AMs, always_exec = True )
def HALT( CPSR, DEST, OPR1, OPR2, RAM ):
    raise HaltExcept
# Does not alter flags
    
@makeOperation( 'NO_OP', 0, AMs = normal_AMs | mem_AMs )
def NO_OP( CPSR, DEST, OPR1, OPR2, RAM ):
    pass
# Does not alter flags
 
@makeOperation( 'CLEAR', 1, AMs = mem_AMs )
def CLEAR( CPSR, DEST, OPR1, OPR2, RAM ):
    val = Register( RAM[OPR2.hept] )
    ALU.CLEAR( val )
    RAM[OPR2.hept] = val.hept
    #RAM[OPR2.hept] = '@@@@@@@@@'
# Does not alter flags
    
@makeOperation( 'LOAD ', 2, AMs = mem_AMs )
def LOAD( CPSR, DEST, OPR1, OPR2, RAM ):
    DEST.hept = RAM[OPR2.hept]
# Does not alter flags
    
@makeOperation( 'STORE', 2, AMs = mem_AMs )
def STORE( CPSR, DEST, OPR1, OPR2, RAM ):
    RAM[OPR2.hept] = DEST.hept
# Does not alter flags
    
@makeOperation( 'EXCH ', 2, AMs = mem_AMs )
def EXCHANGE( CPSR, DEST, OPR1, OPR2, RAM ):
    temp = DEST.hept
    DEST.hept = RAM[OPR2.hept]
    RAM[OPR2.hept] = temp
# Does not alter flags
    
@makeOperation( 'ADD  ', 3 )
def ADD( CPSR, DEST, OPR1, OPR2, RAM ):
    CPSR.C, CPSR.V = ALU.ADD( DEST, OPR1, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the ALL flags according to the new value of DEST
    
@makeOperation( 'SUB  ', 3 )
def SUB( CPSR, DEST, OPR1, OPR2, RAM ):
    CPSR.C, CPSR.V = ALU.SUB( DEST, OPR1, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the ALL flags according to the new value of DEST
    
@makeOperation( 'MOVE ', 2, opr2_update = True )
def MOVE( CPSR, DEST, OPR1, OPR2, RAM ):
    DEST.hept = OPR2.hept
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call
        
@makeOperation( 'AND  ', 3, opr2_update = True )
def AND( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.AND( DEST, OPR1, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call
    
@makeOperation( 'OR   ', 3, opr2_update = True )
def OR( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.OR( DEST, OPR1, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call
    
@makeOperation( 'XOR  ', 3, opr2_update = True )
def XOR( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.XOR( DEST, OPR1, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call
    
@makeOperation( 'F_NOT', 2, opr2_update = True )
def F_NOT( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.F_NOT( DEST, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call
    
@makeOperation( 'N_NOT', 2, opr2_update = True )
def N_NOT( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.N_NOT( DEST, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call
    
@makeOperation( 'T_NOT', 2, opr2_update = True )
def T_NOT( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.T_NOT( DEST, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call

@makeOperation( 'IS_F ', 2, opr2_update = True )
def ISF( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.ISF( DEST, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call
    
@makeOperation( 'IS_N ', 2, opr2_update = True )
def ISN( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.ISN( DEST, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call
    
@makeOperation( 'IS_T ', 2, opr2_update = True )
def IST( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.IST( DEST, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call
    
@makeOperation( 'LSR  ', 3, AMs = normal_AMs - scale_AMs )
def LSR( CPSR, DEST, OPR1, OPR2, RAM ):
    CPSR.C = ALU.LSR( DEST, OPR1, OPR2 )
# Updates the C flag to be the last bit shifted out
    
@makeOperation( 'ASR  ', 3, AMs = normal_AMs - scale_AMs )
def ASR( CPSR, DEST, OPR1, OPR2, RAM ):
    CPSR.C = ALU.ASR( DEST, OPR1, OPR2 )
# Updates the C flag to be the last bit shifted out
    
@makeOperation( 'LSL  ', 3, AMs = normal_AMs - scale_AMs )
def LSL( CPSR, DEST, OPR1, OPR2, RAM ):
    CPSR.C = ALU.LSL( DEST, OPR1, OPR2 )
# Updates the C flag to be the last bit shifted out
    
@makeOperation( 'SHFTM', 2, opr2_update = True )
def SHIFT_M( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.SHIFT_M( DEST, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call
    
@makeOperation( 'SHFTP', 2, opr2_update = True )
def SHIFT_P( CPSR, DEST, OPR1, OPR2, RAM ):
    ALU.SHIFT_P( DEST, OPR2 )
    CPSR.S = ALU.SIGN( DEST )
# Updates the S flag according to the new value of DEST
# Updates the C flag during calculation of OPR2 - happens before function call

@makeOperation( 'JUMP ', 2, AMs = mem_AMs, is_jump = True )
def JUMP( PC_write, DEST, PC_read, OPR2, RAM ):
    PC_write.tern, DEST.tern = OPR2.tern, PC_read.tern
# Does not alter flags
    
OPCODE = {
    '000': HALT,
    '001': NO_OP,
    '002': CLEAR,
    
    '010': LOAD,
    '011': STORE,
    '012': EXCHANGE,
    
    '020': ADD,
    '021': SUB,
    '022': MOVE,
    
    '100': AND,
    '101': OR,
    '102': XOR,
   
    '110': F_NOT,
    '111': N_NOT,
    '112': T_NOT,
   
    '120': ISF,
    '121': ISN,
    '122': IST,
   
    '200': LSR,
    '201': ASR,
    '202': LSL,
   
    '210': SHIFT_M,
    '211': SHIFT_P,
    
    '220': JUMP
}
