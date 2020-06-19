#Image transformation using elastix/transformix
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



#Define base component transformix
def RunTransformix(command):
	"""Run the transfomix deformation. You must be able to call transformix
	from your command shell to use this. You must also have your parameter
	text files set before running (see elastix parameter files).

	command: string to be sent to the system for elastix running (see transformix command line implementation)
	"""

	#Print command
	print(str(command))
	#Print transformix update
	print('Running transformix...')
	#Send the command to the shell
	os.system(command)
	#Print update
	print('Finished')
	#Return values
	return command



#Create class structure for transformix implementation
class Transformix():
	"""Python class for transformix
	"""

	def __init__(self,in,out_dir,tp):
		"""initialize class instance
		"""

		#Create pathlib objects and set class parameters
		self.in = Path(in)
		self.in_channels = []
		self.out_channels = []
		self.multichannel = None
		self.out_dir = Path(out_dir)
		self.tp = Path(tp)
		self.command = "transformix"

		#Load the images to check for dimension number
		print('Loading images...')
	    #Load images
	    niiIn = nib.load(str(self.in))
		#Print update
		print('Done loading')

		#Update the command with the transform parameters
		self.command = self.command + ' -tp ' + str(self.tp)

	    #Check to see if there is single channel input (grayscale)
	    if niiIn.ndim == 2:
			#Update multichannel class option
			self.multichannel = False
			#Remove loaded image to clear memory
			niiIn = None
			#Print update
			print('Detected single channel input images...')
			#Update the command with the single channel path alone
			self.command = self.command + ' -in ' + str(self.in)
			#Update the fixed channels
			self.in_channels.append(self.in)

			#Update the command with the output directory
			self.command = self.command + ' -out ' + str(self.out_dir)
			#Run single channel transformix without temporary directories
			RunTransformix(self.command)

		#Otherwise there is multichannel input
		else:
			#Update multichannel class option
			self.multichannel = True

			#create a temporary directory using the context manager for channel-wise images
			with tempfile.TemporaryDirectory(dir=self.out_dir) as tmpdirname:
				#Print update
				print('Created temporary directory', tmpdirname)
				#Read the image
				niiIn = niiIn.get_fdata()

				#Iterate through the channels
		        for i in range(niiIm.shape[2]):
		            #Create a name for a temporary image
		            im_name = Path(os.path.join(tmpdirname,self.in.stem+str(i)+self.in.suffix))
					#Update the list of names for image channels
					self.in_channels.append(im_name)

					#Check to see if the path exists
					if not im_name.is_file():
						#Create a nifti image from this slice
						nii_im = nib.Nifti1Image(niiIn[:,:,i], affine=np.eye(4))
						#Save the nifti image
						nib.save(nii_im,str(im_name))
						#Remove the nifti slice to clear memory
						nii_im = None

					#Create a temporary command to be sent to the shell
					tmp_command = self.command + ' -in ' + str(im_name) + ' -out ' + str(tmpdirname)
					#Send the command to the shell
					RunTransformix(tmp_command)

					#Get a temporary result name for the output of transformix (assumes nifti for now)
					res_name = Path(os.path.join(tmpdirname,"result"+self.in.suffix))
					#Create a new name
					new_name = Path(os.path.join(tmpdirname,self.in.stem+str(i)+'_result'+self.in.suffix)))
					#Get the resulting image to rename (so we don't overwrite results)
					res_name.rename(new_name) if res_name.is_file(): else raise(ValueError('No transformix results found!'))
					#Update the list of output channel names
					self.out_channels.append(new_name)

				#Remove loaded image to clear memory
				niiIn = None
				#Concatenate the output channels into a single result file in the output directory
				full_result = nib.concat_images([str(i) for i in self.out_channels])
				#create a filename for the full nifti results
				full_name = Path(os.path.join(self.out_dir,self.in.stem+"_result.nii"))
				#Write the results to a nifti file
				nib.save(full_result,full_name)

		#Return the command
		return self.command
