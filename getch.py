#----------------------------------------------------------------
# Author: Olexiy Shkarupa
# e-mail: shkaph@gmail.com
# 6/15/2016
#----------------------------------------------------------------

class Getch:
    # --- Gets a single character from standard input.  Does not echo to the screen. ---
    def __init__(self):
        try:
            self.impl = WindowsImpl()
        except ImportError:
            self.impl = UnixImpl()

    def __call__(self): 
        return self.impl()

class UnixImpl:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class WindowsImpl:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

if __name__ == '__main__':
    print '"getch" module' 
