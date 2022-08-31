from ast import Num
from io import StringIO
import os
import sys
from typing import Any
import unittest

class Capture(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout

def test(testFunc: Any, inputdir: str = '../input', outputdir: str = '../output', verbose: bool = False) -> int:
        failAll = False
        failed = 0
        # note func doesnt return the value, it needs to be read from stdout
        stdin = None

        def dirJoin(dir, rel):
            return os.path.join(dir, rel)

        dir = os.path.dirname(__file__)

        inTsts = []
        outTsts = []

        inDir = dirJoin(dir, inputdir)
        outDir = dirJoin(dir, outputdir)

        # get all input files
        for path in os.listdir(inDir):
            if os.path.isfile(os.path.join(inDir, path)):
                inTsts.append(dirJoin(inDir, path))

        # get all output files
        for path in os.listdir(outDir):
            if os.path.isfile(os.path.join(outDir, path)):
                outTsts.append(dirJoin(outDir, path))

        # iterate over all tests
        for i in range(len(inTsts)):
            inputFile = inTsts[i]
            outputFile = outTsts[i]
            print(f'Attempting test case {i}: {inTsts[i]}')

            stdout = None
            expstdout = ''

            with open(inputFile, 'r') as inLinesIO:
                with open(outputFile, 'r') as outLinesIO:
                    with Capture() as stdout: # capture stdout
                        # store a backup of stdin
                        stdin = sys.stdin

                        # read lines from the files
                        inWrite = ''.join(inLinesIO.readlines())
                        expstdout = ''.join(outLinesIO.readlines()).replace('\n', ' ')

                        # redirect stdin object, and write to it
                        sys.stdin = StringIO(inWrite)
                        
                        # call the passed in function
                        testFunc()

                        # restore stdin
                        sys.stdin = stdin
                        del stdin
            
            # stdout is a list at this point
            output = ' '.join(stdout)
            result = output == expstdout
            failAll |= not result
            failed += 1 if output != expstdout else 0
            print(f'Test case {i}: {("PASSING" if result else "FAILING")}')
            print('===============================================================')
        
        print('Tests complete.')
        print(f"Failed {failed} tests.")

        return 0 if failAll else 1