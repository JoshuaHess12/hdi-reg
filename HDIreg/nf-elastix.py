#Image registration using elastix
#Joshua Hess

#Import modules
import numpy as np
import sys
import time
import os
import re
import nibabel as nib
from pathlib import Path
import pandas as pd
import tempfile

#Import external modules
import elastix



#Add main elastix component
def CompositionElastix(command):
	"""
	Run the elastix registration. You must be able to call elastix
	from your command shell to use this. You must also have your parameter
	text files set before running (see elastix parameter files).

	command: string to be sent to the system for elastix running (see elastix command line implementation)
	"""

	#Print elastix update
	print('Running elastix...')
	#Start timer
	start = time.time()
	#Send the command to the shell
	os.system(command)
	#Stop timer
	stop = time.time()
	#Print update
	print('Finished -- computation took '+str(stop-start)+'sec.')
	#Return values
	return command
