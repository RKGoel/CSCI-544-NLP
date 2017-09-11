import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('1')
    f.add_state('2')
    f.add_state('3')
    f.add_state('4')
    f.add_state('5')
    f.add_state('6')
    f.add_state('7')
    f.add_state('8')
    f.add_state('9')
    f.add_state('10')
    f.add_state('11')
    f.add_state('12') # This state handles numbers 100 and above
    f.initial_state = '1'

    for ii in xrange(10):
        f.add_arc('3', '4', [str(ii)], [kFRENCH_TRANS[ii]])
        if ii == 0:
            f.add_arc('1', '2', [str(ii)], [])
            f.add_arc('2', '3', [str(ii)], [])
            f.add_arc('12', '11', [str(ii)], [])
            f.add_arc('9', '10', [str(ii)], [])
            f.add_arc('11', '10', [str(ii)], [])
        elif ii == 1:
            f.add_arc('9', '10', [str(ii)], [kFRENCH_AND+' '+kFRENCH_TRANS[ii]])
        else:
            f.add_arc('9', '10', [str(ii)], [kFRENCH_TRANS[ii]])
        # to handle 80 - 89
        if not ii == 0:
            f.add_arc('11', '10', [str(ii)], [kFRENCH_TRANS[ii]])
        
        if ii == 1:
            f.add_arc('1', '12', [str(ii)], [kFRENCH_TRANS[100]])
            f.add_arc('2', '5', [str(ii)], [])
            f.add_arc('2', '7', [str(ii)], [kFRENCH_TRANS[10]])
            f.add_arc('12', '5', [str(ii)], [])
            f.add_arc('12', '7', [str(ii)], [kFRENCH_TRANS[10]])
        if ii >= 2 and ii <= 9:
            f.add_arc('1', '12', [str(ii)], [kFRENCH_TRANS[ii]+' '+kFRENCH_TRANS[100]])
        if ii <= 6:
            f.add_arc('5', '6', [str(ii)], [kFRENCH_TRANS[ii+10]])
            if ii == 1:
                f.add_arc('8', '6', [str(ii)], [kFRENCH_AND+' '+kFRENCH_TRANS[ii+10]])
            else:
                f.add_arc('8', '6', [str(ii)], [kFRENCH_TRANS[ii+10]])
        else:
            f.add_arc('7', '6', [str(ii)], [kFRENCH_TRANS[ii]])
        
        if ii >= 2 and ii <= 6:
            f.add_arc('2', '9', [str(ii)], [kFRENCH_TRANS[ii * 10]])
            f.add_arc('12', '9', [str(ii)], [kFRENCH_TRANS[ii * 10]])
        
        if ii == 8:
            f.add_arc('2', '11', [str(ii)], [kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20]])
            f.add_arc('12', '11', [str(ii)], [kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20]])
            
        if ii == 7:
            f.add_arc('2', '8', [str(ii)], [kFRENCH_TRANS[60]])
            f.add_arc('2', '7', [str(ii)], [kFRENCH_TRANS[60]+' '+kFRENCH_TRANS[10]])
            f.add_arc('12', '8', [str(ii)], [kFRENCH_TRANS[60]])
            f.add_arc('12', '7', [str(ii)], [kFRENCH_TRANS[60]+' '+kFRENCH_TRANS[10]])
            
        if ii == 9:
            f.add_arc('2', '5', [str(ii)], [kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20]])
            f.add_arc('2', '7', [str(ii)], [kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20]+' '+kFRENCH_TRANS[10]])
            f.add_arc('12', '5', [str(ii)], [kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20]])
            f.add_arc('12', '7', [str(ii)], [kFRENCH_TRANS[4]+' '+kFRENCH_TRANS[20]+' '+kFRENCH_TRANS[10]])
            

    f.set_final('4')
    f.set_final('6')
    f.set_final('10')

    return f

if __name__ == '__main__':
    #string_input = raw_input()
    for i in xrange(1000):
        #user_input = int(string_input)
        user_input = i
        f = french_count()
        #if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
        #print prepare_input(235)
