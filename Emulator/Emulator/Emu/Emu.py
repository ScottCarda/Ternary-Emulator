from collections import defaultdict
from ..Register import Register, WORD_SIZE, TRYTE_TRYB
from ..CPSR import CPSR

from ..Exceptions import PCOverflowException

#ADDR_SIZE = WORD_SIZE # Number of trytes for address space
#INSTR_SIZE = WORD_SIZE # Number of trytes in an instruction

class Emu(object):

    '''
    27 trits
  xxx   xxx  x  xx  xx  xx   xx   x  xx-xxxxxxxxx
 cond opcode s arg1 AM arg2 arg3 shf  val 
               dest    opr1 opr2
    
Conditions:
    
    000:    Always
    001:    Equal ( S flag = 1 )
    002:    Carry Clear ( C flag = 0 )
    010:    Negative ( S flag = 0 )
    011:    Overflow Clear ( V flag = 0 )
    012:    Unsigned Lower ( C flag = 0, OR S flag = 1 )
    020:    < ( IS_F(S flag) = IS_F(V flag) )    
    021:    <= ( S flag = 1 OR IS_F(S flag) = IS_F(V flag) )
    
    022-200:   <bad>
    
    201:    > ( S flag = 1 AND IS_F(S flag) != IS_F(V flag) )
    202:    >= ( IS_F(S flag) != IS_F(V flag) )
    210:    Unsigned Higher ( C flag != 0 AND S flag != 1 )
    211:    Overflow Set ( V flag != 0 )
    212:    Positive ( S flag != 0 ) - maybe: ( S flag = 2 )
    220:    Carry Set ( C flag != 0 )
    221:    Not Equal ( S flag != 1 )
    222:    Never
        
Shift Values:

    0: LSR
    1: ASR
    2: LSL
        
Address Modes (AM):
    
    00:     Immediate -         Data found in Instruction ( val ) - Ignore opr2 and shf
        MOV     r0, #3          000 022 0 00 00 xx xx x 00-000000010 = 00002200000xxxxx00000000010
        ADD     r0, r1, #3      000 020 0 00 00 01 xx x 00-000000010 = 0000200000001xxx00000000010
        
    01:     Reg Direct -        Register of Data found in Instruction ( opr2 ) - Ignore shf and val
        MOV     r0, r1          000 022 0 00 01 xx 01 x xx-xxxxxxxxx = 00002200001xx01xxxxxxxxxxxx
        
    02:     Reg Dir Scalled -   Register of Data and Scale found in Instruction ( val )
        ADD     r0, r1, r2, LSL #15
                                000 020 0 00 02 01 02 2 00-000000120 = 000020000020102200000000120
    
    10:     <bad>
        
    11:     Addressed -         Address of Data found in Instruction ( val ) - Ignore opr1, opr2, and shf
        LDR     r0, [#<address>]
                                000 010 0 00 11 xx xx x ss-<address> = 00001000011xxxxxss<address>
        
    12:     Reg Indirect -      Address of Data stored in Register found in Instruction ( opr1 ) - Ignore opr2, shf, and val
        LDR     r0, [r1]        000 010 0 00 12 01 xx x xx-xxxxxxxxx = 0000100001201xxxxxxxxxxxxxx
        
    20:     -w/ Imm Offset -    Reg Indirect Address plus Offset found in Instruction ( Reg: opr1, Off: val ) - Ignore opr2 and shf
        LDR     r0, [r1, #3]    000 010 0 00 20 01 xx x 00-000000010 = 0000100002001xxx00000000010
        
    21:     -w/ Dir Offset -    Reg Indirect Address plus Offset found in Reg in Instruction ( Reg: opr1, Off: opr2 ) - Ignore shf and val
        LDR     r0, [r1, r2]    000 010 0 00 21 01 02 x xx-xxxxxxxxx = 000010000210102xxxxxxxxxxxx
                                
    22:     -w/ Scaled Offset - Reg Indirect Address plus Scaled Offset found in Reg in Instruction, Scale is found in Instruction
                                ( Reg: opr1, Off: opr2, Scale: val )
        LDR     r0, [r1, r2, LSL #1]
                                000 010 0 00 22 01 02 2 00-000000001 = 000010000220102200000000001
    
Opcodes:

    (@) 000: HALT
    (A) 001: NO_OP
    (B) 002: CLEAR

    (C) 010: LOAD
    (D) 011: STORE
    (E) 012: EXCHANGE

    (F) 020: ADD
    (G) 021: SUB
    (H) 022: MOVE

    (I) 100: AND
    (J) 101: OR
    (K) 102: XOR

    (L) 110: F_NOT
    (M) 111: N_NOT
    (N) 112: T_NOT

    (O) 120: ISF
    (P) 121: ISN
    (Q) 122: IST

    (R) 200: LSR
    (S) 201: ASR
    (T) 202: LSL

    (U) 210: SHIFT_M
    (V) 211: SHIFT_P
    (W) 212: <bad>

    (X) 220: JUMP
    (Y) 221: <bad>
    (Z) 222: <bad>

    '''
    
    from .InOut import  \
        read_object,    \
        print_ram,      \
        print_reg
        
    from .Execution import  \
        start,              \
        do_instr,           \
        print_instr,        \
        print_instr_long
            
    def __init__(self):
        self.register = [Register() for i in range(9)]
        self.register = tuple(self.register)
        
        self.RAM = defaultdict( lambda : '@' * WORD_SIZE * TRYTE_TRYB )
        self.PC = Register()
        self.CPSR = CPSR()
        
        self.verbose = True
        self.verbose_long = True
        #self.debug = True
        self.exec = False
        
    def IncrPC( self ):
        if self.PC.hept == 'Z' * WORD_SIZE * TRYTE_TRYB:
            raise PCOverflowException
        self.PC.val += 1
    
    #def check_cond( self, condition ):
    #    try:
    #        return self.CPSR.cond[condition]()
    #    except KeyError as e:
    #        # should box this is more meaningful custom exception
    #        raise
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
