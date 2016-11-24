#!/bin/python

#----------------------------------------------------------------
# Author: Olexiy Shkarupa
# e-mail: shkaph@gmail.com
# 6/15/2016
#----------------------------------------------------------------

import sys
import re
import subprocess
from getch import Getch


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
    print '(c) Olexiy Shkarupa, 2016'
    print 'Usage:', name , '<input-file-name>'






'''
  Tyt HE MO>|<E ByTu
          |
          v
* x . | X @ . | * . x
x . . | * * * | x x x
* x . | . X X | * . .
------+-------+------
. 1 . | . . . | . x .
. . . | . . . | x 1 .
. . . | . X . | x x x
------+-------+------
. . 1 | . x x | x . .
. . . | . . . | . x 1
. . . | . x . | x . .



x x . | x * * | x . x
. . x | . . . | x 5 x
. 5 x | x x x | . . .
------+-------+------
. x x | x * * | x . x
x x * | x x x | . x *
x x * | . . x | . x *
------+-------+------
x . x | ! . x | * . x
. x x | x x . | * x x
5 x x | . . . | x . x

! <- MO>|<E ByTu Ti/\bKu TyT

'''


def main():
    s = None

    if len(sys.argv) == 2:
        s = Sudoku(sys.argv[1])
    else:
        help(sys.argv[0])
        sys.exit(1)
    
    if not s.read_file():
        print 'File', sys.argv[1], 'is not exist or corrupted'
        sys.exit(1)

    getch = Getch()
    print 'Press any key... ',
    getch()
    print '\nPress any key... ',
    getch()
    print '\nPress any key... ',
    getch()


#    s.output()

'''
    print '[ \033[0;30m' + 'Text' + '\033[0m ]' + '  [ \033[1;30m' + 'Text' + '\033[0m ]' + '  [ \033[4;30m' + 'Text' + '\033[0m ]' + '  [ \033[5;30m' + 'Text' + '\033[0m ]'
    print '[ \033[0;31m' + 'Text' + '\033[0m ]' + '  [ \033[1;31m' + 'Text' + '\033[0m ]' + '  [ \033[4;31m' + 'Text' + '\033[0m ]' + '  [ \033[5;31m' + 'Text' + '\033[0m ]'
    print '[ \033[0;32m' + 'Text' + '\033[0m ]' + '  [ \033[1;32m' + 'Text' + '\033[0m ]' + '  [ \033[4;32m' + 'Text' + '\033[0m ]' + '  [ \033[5;32m' + 'Text' + '\033[0m ]'
    print '[ \033[0;33m' + 'Text' + '\033[0m ]' + '  [ \033[1;33m' + 'Text' + '\033[0m ]' + '  [ \033[4;33m' + 'Text' + '\033[0m ]' + '  [ \033[5;33m' + 'Text' + '\033[0m ]'
    print '[ \033[0;34m' + 'Text' + '\033[0m ]' + '  [ \033[1;34m' + 'Text' + '\033[0m ]' + '  [ \033[4;34m' + 'Text' + '\033[0m ]' + '  [ \033[5;34m' + 'Text' + '\033[0m ]'
    print '[ \033[0;35m' + 'Text' + '\033[0m ]' + '  [ \033[1;35m' + 'Text' + '\033[0m ]' + '  [ \033[4;35m' + 'Text' + '\033[0m ]' + '  [ \033[5;35m' + 'Text' + '\033[0m ]'
    print '[ \033[0;36m' + 'Text' + '\033[0m ]' + '  [ \033[1;36m' + 'Text' + '\033[0m ]' + '  [ \033[4;36m' + 'Text' + '\033[0m ]' + '  [ \033[5;36m' + 'Text' + '\033[0m ]'
    print '[ \033[0;37m' + 'Text' + '\033[0m ]' + '  [ \033[1;37m' + 'Text' + '\033[0m ]' + '  [ \033[4;37m' + 'Text' + '\033[0m ]' + '  [ \033[5;37m' + 'Text' + '\033[0m ]'
    print ''
    print '[ \033[0;40m' + 'Text' + '\033[0m ]' + '  [ \033[1;40m' + 'Text' + '\033[0m ]' + '  [ \033[4;40m' + 'Text' + '\033[0m ]' + '  [ \033[5;40m' + 'Text' + '\033[0m ]'
    print '[ \033[0;41m' + 'Text' + '\033[0m ]' + '  [ \033[1;41m' + 'Text' + '\033[0m ]' + '  [ \033[4;41m' + 'Text' + '\033[0m ]' + '  [ \033[5;41m' + 'Text' + '\033[0m ]'
    print '[ \033[0;42m' + 'Text' + '\033[0m ]' + '  [ \033[1;42m' + 'Text' + '\033[0m ]' + '  [ \033[4;42m' + 'Text' + '\033[0m ]' + '  [ \033[5;42m' + 'Text' + '\033[0m ]'
    print '[ \033[0;43m' + 'Text' + '\033[0m ]' + '  [ \033[1;43m' + 'Text' + '\033[0m ]' + '  [ \033[4;43m' + 'Text' + '\033[0m ]' + '  [ \033[5;43m' + 'Text' + '\033[0m ]'
    print '[ \033[0;44m' + 'Text' + '\033[0m ]' + '  [ \033[1;44m' + 'Text' + '\033[0m ]' + '  [ \033[4;44m' + 'Text' + '\033[0m ]' + '  [ \033[5;44m' + 'Text' + '\033[0m ]'
    print '[ \033[0;45m' + 'Text' + '\033[0m ]' + '  [ \033[1;45m' + 'Text' + '\033[0m ]' + '  [ \033[4;45m' + 'Text' + '\033[0m ]' + '  [ \033[5;45m' + 'Text' + '\033[0m ]'
    print '[ \033[0;46m' + 'Text' + '\033[0m ]' + '  [ \033[1;46m' + 'Text' + '\033[0m ]' + '  [ \033[4;46m' + 'Text' + '\033[0m ]' + '  [ \033[5;46m' + 'Text' + '\033[0m ]'
    print '[ \033[0;47m' + 'Text' + '\033[0m ]' + '  [ \033[1;47m' + 'Text' + '\033[0m ]' + '  [ \033[4;47m' + 'Text' + '\033[0m ]' + '  [ \033[5;47m' + 'Text' + '\033[0m ]'
'''

    #print '\033[0;34m-----\033[0;36m-==>>\033[0;37m>  C\033[0;33m O M\033[0;31m P L E\033[0;33m T E\033[0;37m D <\033[0;36m<<==-\033[0;34m-----\033[0m'


    
    #simple_cross_off
    #search_unique

if __name__ == '__main__':
    main()
