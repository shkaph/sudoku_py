#!/bin/python

import sys
import re
import subprocess
''' Another approach is possible:
    to make the import by
--> from subprocess import call
    and invoke the 'call' function without name of packet just like that
--> call(...)
'''

SIZE = 9

class Cell:
    def __init__(self):
        self.stencil = [ i+1  for i in range(SIZE) ]  # this is a list
        self.value = 0
        self.new = False

    def set(self, digit):
        if self.value != 0:
            raise ValueError('Cell has already been set up')
        if digit < 1 or digit > 9:
            raise ValueError('Input value is out of range')
        if not digit in self.stencil:
            raise ValueError('Digit is not exist in stencil')
        self.value = digit
        self.unset(digit)
        self.new = True

    def unset(self, digit):
        if digit in self.stencil:
            self.stencil.remove(digit)

class Grid:
    def __init__(self):
        self.cells = [[0] * SIZE for _ in range(SIZE)]
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j] = Cell()

    def strike_out_row(self, _, y, digit):
        for i in range(SIZE):
            self.cells[i][y].unset(digit)

    def strike_out_col(self, x, _, digit):
        for j in range(SIZE):
            self.cells[x][j].unset(digit)

    def strike_out_sqr(self, x, y, digit):
        X = (x // 3) * 3
        Y = (y // 3) * 3
        for i in range(X, X+3):
            for j in range(Y, Y+3):
                self.cells[i][j].unset(digit)

    def strike_out(self, x, y, digit):
        self.strike_out_row(x, y, digit)
        self.strike_out_col(x, y, digit)
        self.strike_out_sqr(x, y, digit)

    def write_down(self, x, y, digit):
        self.cells[x][y].set(digit)
        self.strike_out(x, y, digit)

class Sudoku:
    def __init__(self, in_file, out_file=None):
        self.in_file = in_file
        self.out_file = out_file
        self.check_out_file_name()
        self.grid = Grid()

    def check_out_file_name(self):
        if self.out_file == None or self.out_file == '':
            self.out_file = self.in_file + '.out'

    def read_file(self):
        f = open(self.in_file, 'r')
        if not self.parse(f.read()):
            return False
        f.close()
        return True

    # Private
    def parse(self, text):
        pattern = re.compile('\d|\.') # \d - any digit 
        result = pattern.findall(text)
        if len(result) != SIZE ** 2:
            return False
        k = 0
        for k in range(len(result)):
            x = k // SIZE
            y = k % SIZE
            value = result[k]
            if type(value) == str:
                if (value >= '1' and value <= '9'):
                    self.grid.write_down(x, y, int(value));
            elif type(value) == int:
                self.grid.write_down(x, y, value);
        return True

    # Private
    def output(self):
        print '+' + '-------+' * 3
        for i in range(SIZE):
            print '|',
            for j in range(SIZE):
                self.output_cell(i, j)
                if j % 3 == 2:
                    print '|',
            print ''
            if i % 3 == 2:
                print '+' + '-------+' * 3
                
    # Private
    def output_cell(self, i, j):
        c = self.grid.cells[i][j]
        s = None
        if c.value != 0:
            s = str(c.value)
        else:
            s = '.'
        if c.new:
            s = '\033[0;31m' + s + '\033[0m'
            c.new = False
        print s,



def help(name):
    print 'Sudoku v.0.1'
    print 'Usage:', name , '<input-file-name> [<output-file-name>]'




'''
global Getct = _Getch()

class _Getch:
    # --- Gets a single character from standard input.  Does not echo to the screen. ---
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): 
        print 'call'
        return self.impl.call()


class _GetchUnix:
    def __init__(self):
        print 'unix {ctor}'
        import tty, sys

    def call(self):
        print 'unix call'
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        print 'win {ctor}'
        import msvcrt

    def call(self):
        print 'win call'
        import msvcrt
        return msvcrt.getch()
'''

'''
  Tyt HE MO>|<E ByTbI
          |
          v
* X . | X @ . | * . X
X . . | * * * | X X X
* X . | . X X | * . .
------+-------+------
. 1 . | . . . | . X .
. . . | . . . | X 1 .
. . . | . X . | X X X
------+-------+------
. . 1 | . X X | X . .
. . . | . . . | . X 1
. . . | . X . | X . .
'''



def main():
    s = None

    if len(sys.argv) == 2:
        s = Sudoku(sys.argv[1])
    elif len(sys.argv) == 3:
        s = Sudoku(sys.argv[1], sys.argv[2])
    else:
        help(sys.argv[0])
        sys.exit(1)
    
    if not s.read_file():
        print 'File', sys.argv[1], 'is not exist or corrupted'
        sys.exit(1)

    s.output()

    #print '\033[0;34m-----\033[0;36m-==>>\033[0;37m>  C\033[0;33m O M\033[0;31m P L E\033[0;33m T E\033[0;37m D <\033[0;36m<<==-\033[0;34m-----\033[0m'

'''
    ch = _Getch()
    aa = ch()
    print
    print aa
    print
'''
    
    #simple_cross_off
    #search_unique

if __name__ == '__main__':
    main()
