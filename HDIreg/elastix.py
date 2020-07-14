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
import utils



#Add main elastix component
def RunElastix(command):
	"""
	Run the elastix registration. You must be able to call elastix
	from your command shell to use this. You must also have your parameter
	text files set before running (see elastix parameter files).

	command: string to be sent to the system for elastix running (see elastix command line implementation)
	"""

	#Print command
	print(str(command))
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



#Define elastix class structure
class Elastix():
	"""Elastix image registration class
	"""

	def __init__(self,fixed,moving,out_dir,p,fp=None,mp=None,fMask=None):
		"""initialize class instance
		"""

		#Create pathlib objects and set class parameters
		self.fixed = Path(fixed)
		self.fixed_channels = []
		self.moving_channels = []
		self.multichannel = None
		self.moving = Path(moving)
		self.out_dir = Path(out_dir)
		self.temp_dir = None
		self.p = [Path(par_file) for par_file in p]
		self.fp = None if fp is None else Path(fp)
		self.mp = None if mp is None else Path(fp)
		self.fMask = None if fMask is None else Path(fMask)
		self.command = "elastix"

		#Load the images to check for dimension number
		print('Loading images...')
	    #Load images
		niiFixed = nib.load(str(self.fixed))
		niiMoving = nib.load(str(self.moving))
		#Print update
		print('Done loading')

	    #Add the parameter files
		self.command = self.command + ' '.join([" -p "+str(self.p[par_file]) for par_file in self.p])

	    #Check for corresponding points in registration (must have fixed and moving set both)
		if self.fp and self.mp is not None:
			#Add to the command
			self.command = self.command +" -fp "+str(self.fp)+" -mp "+str(self.mp)

	    #Check for fixed mask
		if fMask is not None:
			#Add the fixed mask to the command if it exists
			self.command = self.command +" -fMask "+str(fMask)

	    #Add the output directory to the command
		self.command = self.command +" -out "+str(self.out_dir)

	    #Check to see if there is single channel input (grayscale)
		if niiFixed.ndim == 2 and niiMoving.ndim == 2:
			print('Detected single channel input images...')
	        #Add fixed and moving image to the command string
			self.command = self.command+" -f "+str(self.fixed)+ " -m "+str(self.moving)
			#Update the fixed channels
			self.fixed_channels.append(self.fixed)
			#Update the moving channels
			self.moving_channels.append(self.moving)
			#Update whether this is a multichannel input or not
			self.multichannel = False

			#Run elastix without creating temporary directory
			RunElastix(self.command)

	    #Check to see if there is multichannel input
		else:
			#create a temporary directory using the context manager for channel-wise images
			with tempfile.TemporaryDirectory(dir=self.out_dir) as tmpdirname:
				#Print update
				print('Created temporary directory', tmpdirname)
				#Print update
				print('Exporting single channel images for multichannel input...')
		        #Read the images
				niiFixed = niiFixed.get_fdata()
				niiMoving = niiMoving.get_fdata()
				#Update multichannel class option
				self.multichannel = True

				#Export single channel images for each channel of fixed image
				for i in range(niiFixed.shape[2]):
					#Create a filename
					fname = Path(os.path.join(tmpdirname,str(self.fixed.stem+str(i)+self.fixed.suffix)))
					#Update the list of names for fixed image
					self.fixed_channels.append(fname)
					#Update the list of names for fixed image
					self.command = self.command + ' -f' + str(i) + ' ' + str(fname)
					#Check to see if the path exists
					if not fname.is_file():
						#Create a nifti image
						nii_im = nib.Nifti1Image(niiFixed[:,:,i], affine=np.eye(4))
						#Save the nifti image
						nib.save(nii_im,str(fname))

				#Remove the fixed image from memory
				niiFixed = None

				#Export single channel images for each channel of fixed image
				for i in range(niiMoving.shape[2]):
					#Create a filename
					mname = Path(os.path.join(tmpdirname,str(self.moving.stem+str(i)+self.moving.suffix)))
					#Update the list of names for moving image
					self.moving_channels.append(mname)
					#Update the list of names for moving image
					self.command = self.command + ' -m' + str(i) + ' ' + str(mname)
					#Check to see if the path exists
					if not mname.is_file():
						#Create a nifti image
						nii_im = nib.Nifti1Image(niiMoving[:,:,i], affine=np.eye(4))
						#Save the nifti image
						nib.save(nii_im,str(mname))

				#Remove the moving image from memory
				niiMoving = None
				#Run the command using the function created
				RunElastix(self.command)

		#Return the command itself
		#return self.command
