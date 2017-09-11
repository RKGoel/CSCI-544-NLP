from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    """
    Returns an FST that converts letters to numbers as specified by
    the soundex algorithm
    """
    
    # define all groups
    grp0 = ['a', 'e', 'h', 'i', 'o', 'u', 'w', 'y', 'A', 'E', 'H', 'I', 'O', 'U', 'W', 'Y']
    grp1 = ['b', 'f', 'p', 'v', 'B', 'F', 'P', 'V']
    grp2 = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z', 'C', 'G', 'J', 'K', 'Q', 'S', 'X', 'Z']
    grp3 = ['d', 't', 'D', 'T']
    grp4 = ['l', 'L']
    grp5 = ['m', 'n', 'M', 'N']
    grp6 = ['r', 'R']

    # Let's define our first FST
    f1 = FST('soundex-generate')

    # Add states for each group
    # state zero is for vowels
    # Assign start
    f1.add_state('start')
    f1.add_state('0')
    f1.add_state('1')
    f1.add_state('2')
    f1.add_state('3')
    f1.add_state('4')
    f1.add_state('5')
    f1.add_state('6')
    f1.initial_state = 'start'

    # Set all the final states
    f1.set_final('0')
    f1.set_final('1')
    f1.set_final('2')
    f1.set_final('3')
    f1.set_final('4')
    f1.set_final('5')
    f1.set_final('6')

    # Add the rest of the arcs
    for letter in string.ascii_letters:
        if letter in grp0:
            f1.add_arc('start', '0', (letter), (letter))
            for i in range(0,7):
                f1.add_arc(str(i), '0', (letter), ())
        if letter in grp1:
            f1.add_arc('start', '1', (letter), (letter))
            for i in range(0,7):
                if i != 1:
                    f1.add_arc(str(i), '1', (letter), ('1'))
                else:
                    f1.add_arc(str(i), '1', (letter), ())
        if letter in grp2:
            f1.add_arc('start', '2', (letter), (letter))
            for i in range(0,7):
                if i != 2:
                    f1.add_arc(str(i), '2', (letter), ('2'))
                else:
                    f1.add_arc(str(i), '2', (letter), ())
        if letter in grp3:
            f1.add_arc('start', '3', (letter), (letter))
            for i in range(0,7):
                if i != 3:
                    f1.add_arc(str(i), '3', (letter), ('3'))
                else:
                    f1.add_arc(str(i), '3', (letter), ())
        if letter in grp4:
            f1.add_arc('start', '4', (letter), (letter))
            for i in range(0,7):
                if i != 4:
                    f1.add_arc(str(i), '4', (letter), ('4'))
                else:
                    f1.add_arc(str(i), '4', (letter), ())
        if letter in grp5:
            f1.add_arc('start', '5', (letter), (letter))
            for i in range(0,7):
                if i != 5:
                    f1.add_arc(str(i), '5', (letter), ('5'))
                else:
                    f1.add_arc(str(i), '5', (letter), ())
        if letter in grp6:
            f1.add_arc('start', '6', (letter), (letter))
            for i in range(0,7):
                if i != 6:
                    f1.add_arc(str(i), '6', (letter), ('6'))
                else:
                    f1.add_arc(str(i), '6', (letter), ())
    return f1


def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')

    # Indicate initial and final states
    f2.add_state('1')
    f2.add_state('2')
    f2.add_state('3')
    f2.add_state('4')
    f2.add_state('5')
    f2.initial_state = '1'
    
    # set any state as final state
    # string can have less than 3 digits
    f2.set_final('2')
    f2.set_final('3')
    f2.set_final('4')
    f2.set_final('5')

    # Add the arcs
    for letter in string.ascii_letters:
        f2.add_arc('1', '2', (letter), (letter))

    for n in range(10):
        f2.add_arc('2', '3', (str(n)), (str(n)))
        f2.add_arc('3', '4', (str(n)), (str(n)))
        f2.add_arc('4', '5', (str(n)), (str(n)))
        f2.add_arc('5', '5', (str(n)), ())

    return f2


def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')

    f3.add_state('1')
    f3.add_state('2')
    f3.add_state('3')
    f3.add_state('4')
    f3.add_state('5')
    f3.add_state('6')
    f3.add_state('7')
    
    f3.initial_state = '1'
    f3.set_final('5')

    for letter in string.ascii_letters:
        f3.add_arc('1', '2', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('2', '3', (str(number)), (str(number)))
        f3.add_arc('3', '4', (str(number)), (str(number)))
        f3.add_arc('4', '5', (str(number)), (str(number)))
    
    # for 3 zeroes padded
    f3.add_arc('2', '6', (), ('0'))
    f3.add_arc('6', '7', (), ('0'))
    f3.add_arc('7', '5', (), ('0'))
    
    # for 2 zeroes padded
    f3.add_arc('3', '7', (), ('0'))
    # arc from 7 to 5 is already added
    
    # for 1 zero padded
    f3.add_arc('4', '5', (), ('0'))
    
    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
