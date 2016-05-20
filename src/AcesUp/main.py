#!/usr/bin/python

import sys
from AcesUp import AcesUp

game = AcesUp()
exitCode = game.main(len(sys.argv), str(sys.argv))

print('\nAcesUp exited with status: ' + str(exitCode) + '\nThanks for playing!\n')
