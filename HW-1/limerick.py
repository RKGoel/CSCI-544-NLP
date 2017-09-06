#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()


    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        # TODO: provide an implementation!
        # Retreive the pronunciations of the given word
        pronunciations = self._pronunciations.get(word.lower())
        
        # If word is not found in dict, return 1
        if (pronunciations == None):
            return 1
        
        # Initialize number of syllables with maxint
        count = sys.maxint
        
        # Check for all possible pronunciations...
        for pronunciation in pronunciations:
            temp_count = 0
            for phoneme in pronunciation:
                if(phoneme[-1].isdigit()):
                    temp_count += 1
            if (count > temp_count):
                count = temp_count     
        
        # count has number of syllables in
        # shortest length pronunciation. Return it 
        return count
        
    def normalize(self, pronunciations):
        norm_pronunciations = []
        for pronunciation in pronunciations:
            while (not pronunciation[0][-1].isdigit()):
                del pronunciation[0]
            norm_pronunciations.append(pronunciation)
        return norm_pronunciations

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        # TODO: provide an implementation!
        pronunciations_a = self._pronunciations.get(a.lower())
        pronunciations_b = self._pronunciations.get(b.lower())
        
        if (pronunciations_a == None or pronunciations_b == None):
            return False
        
        # Normalize sound sequence of both words by stripping
        # all sounds until first vowel is reached
        norm_pronunciations_a = self.normalize(pronunciations_a)
        norm_pronunciations_b = self.normalize(pronunciations_b)
        
        isRhyme = False
        # For all possible combinations of pronunciations
        for norm_pronunciation_a in norm_pronunciations_a:
            for norm_pronunciation_b in norm_pronunciations_b:
                shorter_pronunciation = list(norm_pronunciation_a)
                longer_pronunciation = list(norm_pronunciation_b)
                if (len(norm_pronunciation_a) > len(norm_pronunciation_b)):
                    shorter_pronunciation = norm_pronunciation_b
                    longer_pronunciation = norm_pronunciation_a
                while (shorter_pronunciation):
                    if (longer_pronunciation[-1] == shorter_pronunciation[-1]):
                        del longer_pronunciation[-1]
                        del shorter_pronunciation[-1]
                    else :
                        break
                if (not shorter_pronunciation):
                    isRhyme = True
                    break
            if (isRhyme):
                break
        
        return isRhyme
        
    def limerick_rhymes(self, last_words):
        

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        # TODO: provide an implementation!
        sents = [sent for sent in text.splitlines()]
        
        #######
        #print sents
        #print len(sents)
        ########
        
        tokenized_sents = [word_tokenize(sent) for sent in sents]
        tokenized_sents = [sent for sent in tokenized_sents if sent != []] # ignores blank lines
        
        # If not exactly 5 sentences after ignoring blank lines
        # then not a limerick, return false
        if (len(tokenized_sents) != 5):
            return False
        
        # Remove words that only have punctuations #####
        for i in range(0, len(tokenized_sents)):
            tokenized_sents[i] = [word for word in tokenized_sents[i] if not all(char in punctuation for char in word)]
            
        ########
        print tokenized_sents
        print len(tokenized_sents)
        print "\n-------------------------\n"
        ########
        
        last_words = []
        for i in range(0, len(tokenized_sents)):
            last_words.append(tokenized_sents[i][-1])
        if (not limerick_rhymes(last_words)):
            return False
            
        
        return False


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
