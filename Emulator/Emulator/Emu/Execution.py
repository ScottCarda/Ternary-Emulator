from ..Addressing import ADDRMODES, Rotate_Immediate
from ..Operations import OPCODE
from ..Register import Register, IsHept, HeptToTern, TernToDec
from ..CPSR import CPSR
from .Instruction import Instruction

from ..Exceptions import    \
    EmuExceptionHandler,    \
    EmuException,           \
    BadAddrWithOpException, \
    PCOverflowException,    \
    BadConditionException,  \
    BadAddrException,       \
    BadOpcodeException

def start( self ):

    self.CPSR.clear()
    start_PC = self.PC.hept

    while True:
        try:
            instruction = Instruction( self.RAM[self.PC.hept] )
        
            if self.verbose_long == True:
                self.print_instr_long( instruction, silent = False )
                
            if self.verbose == True:
                self.print_instr( instruction, silent = False )
            
            if self.exec == True or is_always_execute( instruction.opcode, silent = False ):
                self.do_instr( instruction, silent = False )
            else:
                # Handle possible PC Overflow 
                try:
                    self.IncrPC()
                except PCOverflowException as e:
                    print( e.msg )
                    raise
            #print( self.PC.hept )
        except EmuException as e:
            self.PC.hept = start_PC
            return

@EmuExceptionHandler
def is_always_execute( opcode ):
    return OPCODE[opcode].always_exec
        
@EmuExceptionHandler
def do_instr( self, instr ):

    if type( instr ) is not Instruction:
        instr = Instruction( instr )

    #if IsHept( instruction ):
    #    instruction = HeptToTern( instruction )

    # parse instruction 
    #condition = instruction[0:3]
    #opcode = instruction[3:6]
    #set_flag = instruction[6]
    #arg1 = instruction[7:9]
    #addr_mode = instruction[9:11]
    #arg2 = instruction[11:13]
    #arg3 = instruction[13:15]
    #shift_op = instruction[15]
    #val_rot = instruction[16:18]
    #val = instruction[18:27]
    
    try:
        Cond_func = self.CPSR.cond[instr.condition]
    except KeyError:
        raise BadConditionException( instr.condition )
    
    # check the condition
    if not Cond_func():
        self.IncrPC()
        return
        
    try:
        AM_func = ADDRMODES[instr.addr_mode]
    except KeyError:
        raise BadAddrException( instr.addr_mode )
        
    try:
        OP_func = OPCODE[instr.opcode]
    except KeyError:
        raise BadOpcodeException( instr.opcode )
        
    if instr.addr_mode not in OP_func.AMs:
        raise BadAddrWithOpException(
            OP_func.name.strip(),
            instr.opcode,
            AM_func.name.strip(),
            instr.addr_mode
        )
        
    # set up agruments to the operations
    tCPSR = self.CPSR
    tDEST = self.register[TernToDec(instr.arg1)]
    tOPR1 = self.register[TernToDec(instr.arg2)]
    tOPR2 = self.register[TernToDec(instr.arg3)]
    
    # addr_mode determines tOPR2
    tOPR2, carry = AM_func( tOPR1, tOPR2, instr.shift_op, instr.val_rot, instr.val )
    
    if OP_func.is_jump == False:    
        # set flag determines tCPSR and tDEST
        if instr.set_flag == '0':
            tCPSR = CPSR()
        elif instr.set_flag == '2':
            tDEST = Register()
            
        # if the operation sets the carry flag based on the calculation of OPR2
        if carry != -1:
            tCPSR.C = carry
            
    else: # manage jump special case
        # JUMP doesn't modify CPSR or use OPR1, so PC is used instead
        tCPSR = self.PC # This is the one that gets modified
        tOPR1 = self.PC # This is the one that gets read from
    
        # set flag determines tCPSR and tDEST
        if instr.set_flag == '0': # CASE S = '0': don't capture value of PC
            tDEST = Register()
        elif instr.set_flag == '2': # CASE S = '2': don't jump, only capture PC
            tCPSR = Register()
    
    # opcode calls operation with tCPSR, tDEST, tOPR1, tOPR2, and RAM
    OP_func( tCPSR, tDEST, tOPR1, tOPR2, self.RAM )
    
    # increment PC
    if OP_func.is_jump == False:
        self.IncrPC()
    elif instr.set_flag == '2': # If the JUMP just retrieved the PC
        self.IncrPC()

@EmuExceptionHandler
def print_instr_long( self, instr ):

    if type( instr ) is not Instruction:
        instr = Instruction( instr )

    #if IsHept( instruction ):
    #    instruction = HeptToTern( instruction )

    # parse instruction 
    #condition = instruction[0:3]
    #opcode = instruction[3:6]
    #set_flag = instruction[6]
    #arg1 = instruction[7:9]
    #addr_mode = instruction[9:11]
    #arg2 = instruction[11:13]
    #arg3 = instruction[13:15]
    #shift_op = instruction[15]
    #val_rot = instruction[16:18]
    #val = instruction[18:27]
    
    try:
        Cond_func = self.CPSR.cond[instr.condition]
    except KeyError:
        raise BadConditionException( instr.condition )
        
    try:
        AM_func = ADDRMODES[instr.addr_mode]
    except KeyError:
        raise BadAddrException( instr.addr_mode )
        
    try:
        OP_func = OPCODE[instr.opcode]
    except KeyError:
        raise BadOpcodeException( instr.opcode )
    
    # Condition
    print_string = Cond_func.name + ' '
    
    # Opperation
    print_string += OP_func.name + ' '
    
    # Set Flag Letter
    if instr.set_flag == '0':
        print_string += 'N' + ' '
    elif instr.set_flag == '1':
        print_string += 'S' + ' '
    elif instr.set_flag == '2':
        print_string += 'X' + ' '
        
    # Destination Register
    print_string += 'r{0}'.format( TernToDec(instr.arg1) ) + ' '
    
    # Address Mode
    print_string += AM_func.name + ' '
    
    # Oprand1 Register
    print_string += 'r{0}'.format( TernToDec(instr.arg2) ) + ' '
    
    # Oprand2 Register
    print_string += 'r{0}'.format( TernToDec(instr.arg3) ) + ' '
    
    # Shift Operation
    if instr.shift_op == '0':
        print_string += 'LSR' + ' '
    elif instr.shift_op == '1':
        print_string += 'ASR' + ' '
    elif instr.shift_op == '2':
        print_string += 'LSL' + ' '
        
    # Immediate Operand
    print_string += str( Rotate_Immediate( instr.val_rot, instr.val ) )
    
    print( print_string )

@EmuExceptionHandler
def print_instr( self, instr ):
    
    if type( instr ) is not Instruction:
        instr = Instruction( instr )
    
    try:
        Cond_func = self.CPSR.cond[instr.condition]
    except KeyError:
        raise BadConditionException( instr.condition )
    
    # Condition
    if not Cond_func():
        print( Cond_func.name + ': Failed to Meet Condition, Instruction Skipped' )
        return
    
    try:
        AM_func = ADDRMODES[instr.addr_mode]
    except KeyError:
        raise BadAddrException( instr.addr_mode )
        
    try:
        OP_func = OPCODE[instr.opcode]
    except KeyError:
        raise BadOpcodeException( instr.opcode )
        
    if instr.addr_mode not in OP_func.AMs:
        raise BadAddrWithOpException(
            OP_func.name.strip(),
            instr.opcode,
            AM_func.name.strip(),
            instr.addr_mode
        )
        
    # set up agruments to the operations
    tOPR1 = self.register[TernToDec(instr.arg2)]
    tOPR2 = self.register[TernToDec(instr.arg3)]

    # addr_mode determines tOPR2
    tOPR2, _ = AM_func( tOPR1, tOPR2, instr.shift_op, instr.val_rot, instr.val )
    
    # Opperation
    print_string = OP_func.name + ' '
    
    # Set Flag Letter
    if instr.set_flag == '0':
        print_string += 'N' + ' '
    elif instr.set_flag == '1':
        print_string += 'S' + ' '
    elif instr.set_flag == '2':
        print_string += 'X' + ' '
        
    if OP_func.num_args > 0:    
        # Destination Register
        print_string += 'r{0}'.format( TernToDec(instr.arg1) )
    
    if OP_func.num_args > 2:
        print_string += ' r{0}'.format( TernToDec(instr.arg2) )
    
    if OP_func.num_args > 1:
        # Hacky way of determining which address modes result in addresses
        if instr.addr_mode[0] != '0':
            print_string += ' [{0}]'.format( tOPR2.hept )
        else:
            print_string += ' #{0}'.format( tOPR2.signed )
        
    print( print_string )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
