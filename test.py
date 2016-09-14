#===============================================================================
# a text file to illustrate syntax highlighting in EV3Py
#===============================================================================
def main():
    if __name__ == '__main__':
        for x in range(0, 3):   # a comment
            clear_screen()
            y = 3.1415926
            arg1 = 1
            arg2 = 10
            print "this is " + 'iteration' + "%s\n" + \
				  "and pi is equal to %s\n" + \
				  "and add returns %s\n" % (x, y, add(arg1, arg2))
            forward(LEFT, 75)

def add(arg1, arg2):
    return arg1 + arg2

