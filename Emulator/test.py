import sys
from contextlib import contextmanager
from Emulator import Emu

@contextmanager
def tab():
    class StdOut(object):
        def __init__(self,txtctrl):
            self.txtctrl = txtctrl
        def write(self,string):
            self.txtctrl.write('\t' + string)

    old_stdout = sys.stdout
    sys.stdout = StdOut(old_stdout)
    try:
        yield
    finally:
        sys.stdout = old_stdout
    
q = Emu()

print()
if q.read_object( sys.argv[1] ):
    q.exec = True
    q.verbose = True
    q.verbose_long = False
    print( 'Execution:' )
    with tab():
        q.start()
    
    print( '\nRam:' )
    with tab():
        q.print_ram()
    
    print( '\nRegisters:' )
    with tab():
        q.print_reg()
    
    print()
