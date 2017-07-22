from ..Exceptions import RegisterAssignmentError, RegisterSizeError

TRYTE_TRYB = 3 # Number of Trybles in a Tryte, must be pow of 3
TRYB_TRIT = 3 # Number of trits in a Tryble, must be pow of 3

WORD_SIZE = 3 # Number of Trytes in a typical register

class Register(object):
    
    # The size of a register is not meant to be change after object initialization
    
    def __init__(self, val = 0, size = WORD_SIZE):
        self.__val = 0
        self.size = size
        self.val = val
    
    def __str__(self):
        return self.hept
        
    def __repr__(self):
        return "Register('{0}')".format( self.hept )
    
    @property
    def size(self):
        return self.__size
        
    @size.setter
    def size(self, val):
        if type(val) is int and val > 0:
            self.__size = val
            self.val = self.val # resets internal value
        else:
            raise RegisterSizeError
    
    # Alias for size
    @property
    def trytes(self):
        return self.size
        
    @size.setter
    def trytes(self, val):
        self.size = val
    
    @property
    def trybles(self):
        return self.size * TRYTE_TRYB
    
    @property
    def trits(self):
        return self.trybles * TRYB_TRIT
    
    @property
    def val(self):
        return self.__val
        
    @val.setter
    def val(self, val):
        if type(val) is Register:
            self.__val = val.val
        elif IsHept( val ):
            self.__val = HeptToDec( val[-self.trybles:] )
        elif IsTern( val ):
            self.__val = TernToDec( val[-self.trits:] )
        elif type(val) is int:
            if val < 0:
                self.__val = SignedToUnsigned( val, self.trits )
            else:
                self.__val = val % 3**self.trits
        else:
            raise RegisterAssignmentError( val )
            
    @property
    def signed(self):
        return UnsignedToSigned( self.__val, self.trits )
        
    @signed.setter
    def signed(self, val):
        self.val = val
            
    @property
    def hept(self):
        return DecToHept( self.__val, self.trybles )
        
    @hept.setter
    def hept(self, val):
        self.val = val
            
    @property
    def tern(self):
        return DecToTern( self.__val, self.trits )
        
    @tern.setter
    def tern(self, val):
        self.val = val

#### Symbol Sets ####

Heptavigesimal = '@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Decimal = '0123456789'
Ternary = '012'

#### Converters ####

def HeptToDec( hept ):
    dec = 0
    for s in hept.upper():
        dec = 27 * dec
        if s in Heptavigesimal:
            dec += ord(s) - ord('@')
    return dec
    
def DecToHept( dec, digits=0 ):
    dig = 0

    hept = chr(ord('@') + dec % 27)
    dec //= 27
    dig += 1
    while dec > 0 and dig != digits:
        hept = chr(ord('@') + dec % 27) + hept
        dec //= 27
        dig += 1
    
    while dig < digits:
        hept = '@' + hept
        dig += 1
    
    return hept
    
def TernToDec( tern ):
    dec = 0
    for s in tern:
        dec = 3 * dec
        if s in Ternary:
            dec += int(s)
    return dec
    
def DecToTern( dec, digits=0 ):
    dig = 0

    tern = str(dec % 3)
    dec //= 3
    dig += 1
    while dec > 0 and dig != digits:
        tern = str(dec % 3) + tern
        dec //= 3
        dig += 1
    
    while dig < digits:
        tern = '0' + tern
        dig += 1
    
    return tern
    
def TernToHept( tern ):
    digits = len( tern ) // 3
    if len(tern) % 3 != 0:
        digits += 1
    return DecToHept( TernToDec( tern ), digits )
    
def HeptToTern( hept ):
    digits = 3 * len(hept)
    return DecToTern( HeptToDec( hept ), digits )
    
def UnsignedToSigned( unsign, trits ):
    max = 3**trits
    mid = ( max - 1 ) / 2
    return int(( unsign - mid ) % -max + mid)
    
def SignedToUnsigned( sign, trits ):
    max = 3**trits
    return int(( sign + max ) % max)
    
#### Checkers ####
    
def IsHept( hept ):
    if type( hept ) is not str:
        return False
    if len( hept ) == 0:
        return False
    return all( map( lambda x: x in Heptavigesimal, hept.upper() ) )

def IsTern( tern ):
    if type( tern ) is not str:
        return False
    if len( tern ) == 0:
        return False
    return all( map( lambda x: x in Ternary, tern ) )
















