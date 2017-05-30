from ...Register import IsHept, IsTern, HeptToTern, TRYTE_TRYB, TRYB_TRIT, WORD_SIZE

class Instruction(object):
    def __init__( self, instr_str ):
    
        if type( instr_str ) is not str:
            raise TypeError( "Requires String of Ternary Format" )
    
        if IsHept( instr_str ):
            instr_str = HeptToTern( instr_str )
            
        if not IsTern( instr_str ):
            raise ValueError( "Requires String of Ternary Format" )
            
        if len( instr_str ) != TRYTE_TRYB * TRYB_TRIT * WORD_SIZE:
            raise ValueError( "Instruction Must be a Word in Length" )

        self.whole = instr_str
    
        self.condition = instr_str[0:3]
        self.opcode = instr_str[3:6]
        self.set_flag = instr_str[6]
        self.arg1 = instr_str[7:9]
        self.addr_mode = instr_str[9:11]
        self.arg2 = instr_str[11:13]
        self.arg3 = instr_str[13:15]
        self.shift_op = instr_str[15]
        self.val_rot = instr_str[16:18]
        self.val = instr_str[18:27]
        
