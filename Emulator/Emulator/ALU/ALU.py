from . import Gates

#### Addition Unit ####
    
# Adds contents of two registers and stores result, returns overflow trit
def ADD( dest, src1, src2 ):
    
    sign_1 = Gates.SIGN( *[ int( i ) for i in src1.tern ] )
    sign_2 = Gates.SIGN( *[ int( i ) for i in src2.tern ] )
    
    car = 0
    sum = ''
    # Tritwise loop
    for pair in zip( src1.tern[::-1], src2.tern[::-1] ):
        a, b = map( int, pair )
        #res, car = Gates.ADDER( *map( int, pair ), car )
        res, car = Gates.ADDER( a, b, car )
        sum = str(res) + sum
    dest.tern = sum
    
    sign_d = Gates.SIGN( *[ int( i ) for i in dest.tern ] )
    
    over = Gates.AND( Gates.NOT( Gates.XOR( sign_1, sign_2  ) ), Gates.XOR( sign_2, sign_d ) )
    
    return car, over

# dest = src1 - src2
def SUB( dest, src1, src2 ):
    
    sign_1 = Gates.SIGN( *[ int( i ) for i in src1.tern ] )
    sign_2 = Gates.SIGN( *[ int( i ) for i in src2.tern ] )
    
    car = 1
    dif = ''
    # Tritwise loop
    for pair in zip( src1.tern[::-1], src2.tern[::-1] ):
        a, b = map( int, pair )
        b = Gates.NOT( b )
        res, car = Gates.ADDER( a, b, car )
        dif = str(res) + dif
    dest.tern = dif
    
    sign_d = Gates.SIGN( *[ int( i ) for i in dest.tern ] )
    
    over = Gates.AND( Gates.XOR( sign_1, sign_2  ), Gates.NOT( Gates.XOR( sign_2, sign_d ) ) )
    
    #return int(not car), over
    return car, over

#### Shifting Unit ####

'''    
def LSL( dest, src1, src2 ):
    
    res = ''

    # Tritwise loop
    for digit in src1.tern[src2.val:]:
        res += digit
        
    # Append zeros to the left
    res += '0' * src2.val
    
    # Carry is the highest among trits shifted out
    car = Gates.OR( *map( int, src1.tern[:src2.val] ) )
        
    dest.tern = res
    return car
'''

def LSL( dest, src1, src2 ):
    
    # Append zeros to the right
    res = src1.tern + '0' * src2.val
    
    dest.tern = res[src2.val:]

    car = res[:src2.val]
    
    if len(car) != 0:
        # Carry is the last trit shifted out
        car = int( car[-1] )
        return car
    else:
        return 0 # If no shift happened, carry is zero

'''
def LSR( dest, src1, src2 ):
    
    # Start with zeros to the right
    res = '0' * src2.val
    
    # Tritwise loop
    for digit in src1.tern[:-src2.val]:
        res += digit
    car = int(src1.tern[-src2.val])
    
    dest.tern = res
    return car
'''

def LSR( dest, src1, src2 ):

    # Append zeros to the left
    res = '0' * src2.val + src1.tern
    
    dest.tern = res[:-src2.val]
    
    car = res[-src2.val:]
    
    if len(car) != 0:
        # Carry is the last trit shifted out
        car = int( car[0] )
        return car
    else:
        return 0 # If no shift happened, carry is zero

'''
def ASR( dest, src ):
    
    res = ''
    sign = '0'
    # Tritwise loop
    for digit in src.tern[-2::-1]:
        res = digit + res
        if ( digit != '1' ):
            sign = digit
    res = sign + res
    car = int(src.tern[-1])
    dest.tern = res
    return car 
'''

def ASR( dest, src1, src2 ):

    #sign = src1.tern[0]
    
    #sign = '0'
    #if src1.signed < 0:
    #    sign = '2'
    
    sign = str( Gates.SIGN( *[ int( i ) for i in src1.tern ] ) )

    # Append the sign trit to the left
    res = sign * src2.val + src1.tern
    
    # Sign extend if dest reg is bigger size
    dest.tern = sign * ( len( dest.tern ) - len( res[:-src2.val] ) ) + res[:-src2.val]
    
    car = res[-src2.val:]
    
    if len(car) != 0:
        # Carry is the last trit shifted out
        car = int( car[0] )
        return car
    else:
        return 0 # If no shift happened, carry is zero
    
def ROT( dest, src1, src2 ):
    
    val = src2.val % len( src1.tern )
    
    dest.tern = src1.tern[val:] + src1.tern[:val]
    
    car = src1.tern[:val]
    
    if len(car) != 0:
        # Carry is the last trit shifted out
        car = int( car[-1] )
        return car
    else:
        return 0 # If no shift happened, carry is zero
    
#### Logic Unit ####

def N_NOT( dest, src ):

    res = ''
    # Tritwise loop
    for digit in src.tern:
        res += str(Gates.NOT( int(digit) ))
    dest.tern = res
    return
    
def F_NOT( dest, src ):
    
    res = ''
    # Tritwise loop
    for digit in src.tern:
        res += str(Gates.F_NOT( int(digit) ))
    dest.tern = res
    return

def T_NOT( dest, src ):
    
    res = ''
    # Tritwise loop
    for digit in src.tern:
        res += str(Gates.T_NOT( int(digit) ))
    dest.tern = res
    return
    
def SHIFT_M( dest, src ):
    
    res = ''
    # Tritwise loop
    for digit in src.tern:
        res += str(Gates.M_SHFT( int(digit) ))
    dest.tern = res
    return
    
def SHIFT_P( dest, src ):
    
    res = ''
    # Tritwise loop
    for digit in src.tern:
        res += str(Gates.P_SHFT( int(digit) ))
    dest.tern = res
    return
    
def ISF( dest, src ):
    
    res = ''
    # Tritwise loop
    for digit in src.tern:
        res += str(Gates.IS_F( int(digit) ))
    dest.tern = res
    return
    
def ISN( dest, src ):
    
    res = ''
    # Tritwise loop
    for digit in src.tern:
        res += str(Gates.IS_N( int(digit) ))
    dest.tern = res
    return

def IST( dest, src ):
    
    res = ''
    # Tritwise loop
    for digit in src.tern:
        res += str(Gates.IS_T( int(digit) ))
    dest.tern = res
    return

def AND( dest, src1, src2 ):
    
    res = ''
    # Tritwise loop
    for pair in zip( src1.tern, src2.tern ):
        res += str(Gates.AND( *map( int, pair ) ))
    dest.tern = res
    return
    
def OR( dest, src1, src2 ):

    res = ''
    # Tritwise loop
    for pair in zip( src1.tern, src2.tern ):
        res += str(Gates.OR( *map( int, pair ) ))
    dest.tern = res
    return
    
def XOR( dest, src1, src2 ):
    
    res = ''
    # Tritwise loop
    for pair in zip( src1.tern, src2.tern ):
        res += str(Gates.XOR( *map( int, pair ) ))
    dest.tern = res
    return
    
#### Other ####
    
def CLEAR( dest ):
    dest.val = 0
    return
    
# Returns the sign of the value in the register, 0 for positive, 1 for zero, 2 for negative.
def SIGN( reg ):
    
    trits = [ int( i ) for i in reg.tern ]
    
    sign = Gates.SIGN( *trits )
    
    is_zero = Gates.AND( *[ Gates.IS_F( i ) for i in trits ] )
    
    rtrn_val = Gates.AND( Gates.M_SHFT(sign), Gates.NOT(Gates.IS_T(is_zero)) )
    
    return Gates.P_SHFT( rtrn_val )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
