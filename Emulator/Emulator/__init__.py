from .Emu import Emu
from .Register import Register
#from .Exceptions import *

__all__ = [ 'Emu', 'Register']
'''
def go():
    SUB( q, dest, a, b, 0 )
    print( "Unsigned Lower/Equal: " + str(q.cond['012']())  )
    print( "Less Than: " + str(q.cond['020']()) )
    print( "Less Than/Equal: " + str(q.cond['021']()) )
    print( "Greater Than: " + str(q.cond['201']()) )
    print( "Greater Than/Equal: " + str(q.cond['202']()) )
    print( "Unsigned Higher: " + str(q.cond['210']()) )
'''
