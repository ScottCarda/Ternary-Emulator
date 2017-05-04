
def EmuExceptionHandler( func ):
    def wrapper( *args, silent=True, **kwargs ):
        try:
            return func( *args, **kwargs )
        except EmuException as e:
            print( e.msg )
            if not silent:
                raise
            else:
                return
    return wrapper

### Base Exception Classes ###

class TernaryException(Exception):
    pass
    
class EmuException(TernaryException):
    def __init__( self ):
        super().__init__()
        self.msg = "Generic Emu Exception"
    
class RegisterException(TernaryException):
    pass
    
### Register Exceptions ###
    
class RegisterAssignmentError(RegisterException):
    def __init__( self, val ):
        if type(val) == str:
            super().__init__( "'" + val + "'" )
        else:
            super().__init__( val )

class RegisterSizeError(RegisterException):
    pass
    
### Emu Exceptions ###

class HaltingException(EmuException):
    def __init__( self ):
        super().__init__()
        self.msg = "Program has Halted"
        
class OpNotImplementedException(EmuException):
    def __init__( self, op ):
        super().__init__()
        self.msg = "Operation Not Implemented Exception: " + op
        
class BadAddrWithOpException(EmuException):
    def __init__( self, op, op_code, addr_mode, addr_code ):
        super().__init__()
        self.msg = "Incompatible Address Mode with Operation Exception: " + \
            "{0} ({1}) is incompatible with {2} ({3})".format( op, op_code, addr_mode, addr_code )
            
class PCOverflowException(EmuException):
    def __init__( self ):
        super().__init__()
        self.msg = "PC Overflow Exception"
            
class BadConditionException(EmuException):
    def __init__( self, cond ):
        super().__init__()
        self.msg = "Undefinded Condition Code Exception: {0}".format( cond )
        
class BadAddrException(EmuException):
    def __init__( self, addr_mode ):
        super().__init__()
        self.msg = "Undefinded Address Mode Code Exception: {0}".format( addr_mode )
        
class BadOpcodeException(EmuException):
    def __init__( self, op ):
        super().__init__()
        self.msg = "Undefinded Operation Code Exception: {0}".format( op )

class BadAddrFormatException(EmuException):
    def __init__( self, address ):
        super().__init__()
        self.msg = "Bad Address Format Exception: {0}".format( address )
            
class BadFormatException(EmuException):
    def __init__( self, instr, address ):
        super().__init__()
        self.msg = "Bad Instruction Format Exception: {0} attempted at address {1}".format( instr, address )
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
