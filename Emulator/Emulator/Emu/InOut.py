from ..Register import Register, IsHept

from ..Exceptions import    \
    EmuException,           \
    BadAddrFormatException, \
    BadFormatException

def read_object( self, filename ):
    self.RAM.clear()
    try:
        with open( filename, 'r' ) as f:
            addr = Register()
            for line in f:
                line = line.replace( '\n', '' ).replace( '\r', '' )
                line = [ i for i in line.split( ' ' ) if i != '' ]
                if len( line ) > 0:
                    
                    # check for correct address format
                    if not check_format( line[0] ):
                        raise BadAddrFormatException( line[0] )
                        
                    addr.hept = line[0]
                    
                    for instr in line[1:]:
                        # check for correct format first
                        if not check_format( instr ):
                            raise BadFormatException( instr, addr.hept )
                        
                        # box instr in Register to enforce correct size
                        self.RAM[addr.hept] = Register( instr ).hept
                        addr.val += 1
            self.PC.hept = addr.hept
            return True
    except IOError:
        print( 'Error: Could not open {0} for reading.'.format( filename ) )
        return False
    except EmuException as e:
        print( e.msg )
        return False

def check_format( instr ):
    if not IsHept( instr ):
        return False
    if len( instr ) > 9: # 9 characters in a full word
        return False
    return True

def print_ram(self):
    expected = Register()
    for key, val in sorted( self.RAM.items() ):
        if not key == expected.hept:
            print( '...' )
        print( '{0}: {1}'.format( key, val ) )
        expected.hept = key
        expected.val += 1
    return
    
def print_reg(self):
    for i in range( 9 ):
        print ( 'r{0}: {1}'.format( i, self.register[i] ) )
