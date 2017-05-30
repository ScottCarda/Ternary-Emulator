from ..ALU import LSL, LSR, ASR, ROT
from ..Register import Register, TernToDec

'''
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
'''

def IMM( REG1, REG2, SHF, VAL_ROT, VAL ):
    rtrn_reg = Rotate_Immediate( VAL_ROT, VAL )
    return rtrn_reg, 0
IMM.name = 'IMM  '
    
def REG_DIR( REG1, REG2, SHF, VAL_ROT, VAL ):
    rtrn_reg = Register( REG2 ) # Make a copy of the REG2
    return rtrn_reg, 0
REG_DIR.name = 'DIR  '

def REG_DIR_SCL( REG1, REG2, SHF, VAL_ROT, VAL ):
    off = Rotate_Immediate( VAL_ROT, VAL )
    
    if SHF == '0':
        carry = LSR( off, REG2, off )
    elif SHF == '1':
        carry = ASR( off, REG2, off )
    else:
        carry = LSL( off, REG2, off )
        
    return off, carry
REG_DIR_SCL.name = 'DIRSC'
    

    
def ADDR( REG1, REG2, SHF, VAL_ROT, VAL ):
    rtrn_reg = Rotate_Immediate( VAL_ROT, VAL )
    return rtrn_reg, -1
ADDR.name = 'ADDR '
    
def REG_INDIR( REG1, REG2, SHF, VAL_ROT, VAL ):
    rtrn_reg = Register( REG1 ) # Make a copy of the REG1
    return rtrn_reg, -1
REG_INDIR.name = 'INDIR'


    
def IMM_OFF( REG1, REG2, SHF, VAL_ROT, VAL ):
    off = Rotate_Immediate( VAL_ROT, VAL )
    rtrn_reg = Register( REG1.val + off.val )
    return rtrn_reg, -1
IMM_OFF.name = 'IIMOF'
    
def DIR_OFF( REG1, REG2, SHF, VAL_ROT, VAL ):
    rtrn_reg = Register( REG1.val + REG2.val )
    return rtrn_reg, -1
DIR_OFF.name = 'IDROF'

def SCL_OFF( REG1, REG2, SHF, VAL_ROT, VAL ):
    off = Rotate_Immediate( VAL_ROT, VAL )
    
    if SHF == '0':
        LSR( off, REG2, off )
    elif SHF == '1':
        ASR( off, REG2, off )
    else:
        LSL( off, REG2, off )
        
    rtrn_reg = Register( REG1.val + off.val )
    return rtrn_reg, -1
SCL_OFF.name = 'ISCOF'
    
ADDRMODES = {
    '00': IMM,
    '01': REG_DIR,
    '02': REG_DIR_SCL,
    
    '11': ADDR,
    '12': REG_INDIR,
    
    '20': IMM_OFF,
    '21': DIR_OFF,
    '22': SCL_OFF
}

normal_AMs = { '00', '01', '02' }
scale_AMs = { '02', '22' }
mem_AMs = { '11', '12', '20', '21', '22' }

def Rotate_Immediate( val_rot, val ):

    result = Register( val )
    ROT( result, result, Register( 3 * TernToDec( val_rot ) ) )
    return result
    
    
    
    
    
    
    
    
    
    
    
