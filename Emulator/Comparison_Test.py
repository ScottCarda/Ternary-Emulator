from Emulator import Register as reg
from Emulator.CPSR import CPSR
from Emulator.Operations.Operations import SUB

a = reg()
b = reg()
dest = reg()
c = CPSR()

median = reg('M'*9).signed

point_list = [
    -1,
    0,
    1,
    median - 1,
    median,
    -median
]

field_size = len(str(-median))

conditions = [cond for cond in c.cond]
conditions.sort()

print( ( '|' + '*'*(field_size+2) )*2 + '|' + ( '|' + '*'*3 )*16 + '|' )

print( '| {:^{width}} | {:^{width}} ||'.format( 'A', 'B', width = field_size ), end = '' )
print( ' AL|', end = '' )
print( ' EQ|', end = '' )
print( ' CC|', end = '' )
print( ' MI|', end = '' )
print( ' VC|', end = '' )
print( ' LS|', end = '' )
print( ' LT|', end = '' )
print( ' LE|', end = '' )
print( ' GT|', end = '' )
print( ' GE|', end = '' )
print( ' HI|', end = '' )
print( ' VS|', end = '' )
print( ' PL|', end = '' )
print( ' CS|', end = '' )
print( ' NE|', end = '' )
print( ' NV|' )

print( ( '|' + '*'*(field_size+2) )*2 + '|' + ( '|' + '*'*3 )*16 + '|' )

for a_p in point_list:
    a.signed = a_p
    for b_p in point_list:
        b.signed = b_p
        
        SUB( c, dest, a, b, dict() )
        
        print( '| {.signed!s:^{width}} | {.signed!s:^{width}} ||'.format( a, b, width = field_size ), end = '' )
        
        for condcode in conditions:
            print( ' ' + ( 'X' if c.cond[condcode]() else '-' ) + ' |', end = '' )
        print( '' )
        
print( ( '|' + '*'*(field_size+2) )*2 + '|' + ( '|' + '*'*3 )*16 + '|' )
