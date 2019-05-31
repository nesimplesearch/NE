#!/usr/bin/env python
#
# Project: Implementation of the Lemke-Howson algorithm for finding MNE
# Author:  Petr Zemek <s3rvac@gmail.com>, 2009
#

"""Runs a program which computes MNE in the given 2-player game
using the Lemke-Howson algorithm.
"""


import sys
import argparse
import signal
import os
import time


def solve(path):

    try:
        # These imports must be here because of possible
        # SyntaxError exceptions in different versions of python
        # (this program needs python 2.5)
        import src.io
        import src.lh

        # Check program arguments (there should be none)
        '''if len(sys.argv) > 1:
            stream = sys.stderr
            if sys.argv[1] in ['-h', '--help']:
                stream = sys.stdout
            src.io.printHelp(stream)
            return 1'''
        f=open(path,'r')


        # Obtain input matrices from the standard input
        m1, m2 = src.io.parseInputMatrices(f.read())
        f.close()

        # Compute the equilibirum
        eq = src.lh.lemkeHowson(m1, m2)


        # Print both matrices and the result
        src.io.printGameInfo(m1, m2, eq, sys.stdout)

        return 0
    except SyntaxError:
        sys.stderr.write('Need python 2.5 to run this program.\n')
    except Exception,e:
        sys.stderr.write('Error: ' + e.message + '\n')
        return 1

def handler(signum,frame):
    raise Exception('timeout')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', default='1')
    args = parser.parse_args()
    filedir='./gamut_game/'
    filelist=os.listdir(filedir)
    print(filelist)
    file = open('outdata.csv', 'w')
    for name in filelist:
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(60)
            start=time.time()
            solve(filedir+name)
            end=time.time()
            file.write('{},1,{}\n'.format(name,end-start))

        except:
            continue
    file.close()


