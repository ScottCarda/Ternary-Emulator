#### Table Funcs ####

def print_table1( foo ):

    print( 'I|O' )
    print( '-+-' )

    for i in range( 0, 3 ):
        print( str(i) + '|' + str(foo( i )) )

def print_table2( foo ):

    print ( ' |0 1 2' )
    print ( '-+-----' )

    for i in range( 0, 3 ):
        print( i, end = '|' )
        for j in range( 0, 3 ):
            print( foo( i, j ), end = ' ' )
        print()

#### Atomic Gates ####

def _basic_AND( a, b ):
    if a == 0 or b == 0:
        return 0
    if a == 1 or b == 1:
        return 1
    return 2
    
# Multi-input AND gates are just iterations of basic AND
def AND( *args ):
    if len(args) == 0:
        return 0
    if len(args) == 1:
        return args[0]
        
    rtrn_val = _basic_AND( args[0], args[1] )
        
    for a in args[2:]:
        rtrn_val = _basic_AND( rtrn_val, a )
        
    return rtrn_val

def NOT( a ):
    if a == 0:
        return 2
    if a == 1:
        return 1
    return 0
    
def F_NOT( a ):
    if a == 0:
        return 0
    if a == 1:
        return 2
    return 1
    
#### Single Input Gates ####
    
def M_SHFT( a ):
    return NOT( F_NOT( a ) )
    
def P_SHFT( a ):
    return F_NOT( NOT( a ) )
    
def T_NOT( a ):
    return F_NOT( M_SHFT( a ) )
    
def IS_T( a ):
    return AND( T_NOT( a ), a )
    
def IS_N( a ):
    return F_NOT( AND( NOT( a ), a ) )
    
def IS_F( a ):
    return M_SHFT( AND( F_NOT( a ), a ) )
    
#### Two Input Gates ####
    
def _basic_OR( a, b ):
    return NOT( AND( NOT( a ), NOT( b ) ) )

def OR( *args ):
    if len(args) == 0:
        return 1
    if len(args) == 1:
        return args[0]

    rtrn_val = _basic_OR( args[0], args[1] )
        
    for a in args[2:]:
        rtrn_val = _basic_OR( rtrn_val, a )
        
    return rtrn_val
    
def LOC( a, b ):
    return F_NOT( AND(
        AND( a, b ),
        AND( M_SHFT( a ), M_SHFT( b ) )
    ) )
    
def XOR( a, b ):
    return OR(
        AND( NOT( a ), b ),
        AND( a, NOT( b ) )
    )

#### Special Gates ####

# Unary Decoder
def DCDR( a ):
    return IS_F( a ), IS_N( a ), IS_T( a )

# Single Digit Sum Result
def SUM_R( a, b ):
    is_b_f, is_b_n, is_b_t = DCDR( b )
    
    return OR(
        AND( is_b_f, a ),
        AND( is_b_n, P_SHFT(a) ),
        AND( is_b_t, M_SHFT(a) )
    )
    
# Single Digit Sum Carry
def SUM_C( a, b ):
   fa_and_fb = AND( F_NOT(a), F_NOT(b) )
   return AND( fa_and_fb, NOT( fa_and_fb ) )
   
# Half Adder
def H_ADDER( a, b ):
    return SUM_R( a, b ), SUM_C( a, b )
    
# Full Adder
def ADDER( a, b, c = 0 ):
    res, car1 = H_ADDER( a, b )
    res, car2 = H_ADDER( res, c )
    return res, OR( car1, car2 ) # could do SUM_R( car1, car2 ) but expensive
    
def _basic_SIGN( a, b ):
    #return OR( AND( a, NOT( n_a ) ), AND( n_a, b ) )
    return OR( IS_T( a ), AND( IS_N( a ), b ) )
    
# Multi-input SIGN gates combine basic SIGN gates then perform IS_T
def SIGN( *args ):
    if len(args) == 0:
        return 1
    if len(args) == 1:
        return args[0]
        
    rtrn_val = _basic_SIGN( args[0], args[1] )
        
    for a in args[2:]:
        rtrn_val = _basic_SIGN( rtrn_val, a )
    
    return IS_T( rtrn_val )
    #rtrn_val = IS_T( rtrn_val )
    #is_zero = AND(*map(IS_F, args))
    
    #rtrn_val = AND( M_SHFT(rtrn_val), NOT(IS_T(is_zero)) )
    
    #return P_SHFT( rtrn_val )






























    
