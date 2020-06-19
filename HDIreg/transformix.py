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



class Transformix():
	"""Python class for transformix
	"""

	def __init__(self,in,out_dir,tp):
		"""initialize class instance
		"""

		#Create pathlib objects and set class parameters
		self.in = Path(in)
		self.in_channels = []
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

	    #Check to see if there is single channel input (grayscale)
	    if niiIn.ndim == 2:
			print('Detected single channel input images...')
			#Update the command with the single channel path alone
			self.command = self.command + ' -in ' + str(self.in)
			#Update multichannel class option
			self.multichannel = False
			#Update the fixed channels
			self.in_channels.append(self.in)

		#Otherwise there is multichannel input
		else:
			#Update multichannel class option
			self.multichannel = True

		#Remove loaded image to clear memory
		niiIn = None

		#Update the command with the transform parameters
		self.command = self.command + ' -tp ' + str(self.tp)
		#Update the command with the output directory
		self.command = self.command + ' -out ' + str(self.out_dir)

		#Return the command
		return self.command


	#Definition for running transformix given input command
	def RunTransformix(self):
		"""Function for running transformix given the input command.
		Run the transfomix call. You must be able to call elastix
		from your command shell to use this. You must also have your parameter
		text files set before running (see elastix parameter files).

		Currently supports nifti1image format only!
		"""

		#Check if the input is multichannel
		if self.multichannel:
			#Read the image
			niiIm = nib.load(str(self.in)).get_fdata()
			#Iterate through the channels
	        for i in range(niiIm.shape[2]):
	            #Get the image name from your input image path
	            im_name=Path(tmp_data.filename).parts[-1]
	            #Remove the file extension
	            prefix,extension=Path(im_name).stem,Path(im_name).suffix
	            #Create new image channel i in each iteration
	            nifti_col = nib.Nifti1Image(tmp_data[:,:,i], affine=np.eye(4))
	            #Create the image path for this iteration
	            tmp_image=prefix+"_Unregistered"+str(i)+extension
	            #Save the nifti image
	            print("Saving a temporary image for channel "+str(i)+"...")
	            nib.save(nifti_col,str(tmp_image))
	            #Now load the image and run transformix on that channel in the shell
	            print("Running Transformix for channel "+str(i)+"...")
	            #Creat a new file for your transformix results
	            transformix_path = Path(os.path.join(str(output_dir),str(prefix)+"_Transformix_Registered"+str(i)))
	            transformix_path.mkdir()
	            os.system("transformix -in " +str(tmp_image)+ " -out "+str(transformix_path)+" -tp "+str(parameter_file))
	            print("Finished Transforming Channel "+str(i))
	            #add filenames to the list
	            filenames_channels.append(os.path.join(str(transformix_path),"result.nii"))

		#Otherwise run transformix for the single channel
		else:
			#Print command
			print(str(self.command))
			#Print elastix update
			print('Running transformix...')
			#Start timer
			start = time.time()
		    #Send the command to the shell
		    os.system(self.command)
			#Stop timer
			stop = time.time()
			#Print update
			print('Finished -- computation took '+str(stop-start)+'sec.')





def TransformixRegistration(input_img,output_dir,parameter_file,conc=False,points=None):
    """This is a python function for running transformix image registration. Again,
    must be able to call elastix from the command line to be able to run this.

    If your channel is multichannel, this script must first export each channel
    in the nifti format. By default, images will be exported to your output_dir
    and will include the suffix 'Unregistered' followed by the channel number"""
    #Create a timer
    trans_start = time.time()
    #Check to see if the image is multichannel or grayscale (note: need to remove " in your filename)
    tmp_data = nib.load(str(input_img)).get_data()
    if tmp_data.ndim is not 2:
        print('Detected multichannel image. Creating channel images...')
        #Get the current directory
        tmp_path = Path('..')
        home_dir=tmp_path.cwd()
        #Set the working directory as the output directory
        parent=Path(output_dir)
        os.chdir(parent)
        #Now take each of the channels and export a separate image for registration
        filenames_channels = []
        for i in range(tmp_data.shape[2]):
            #Get the image name from your input image path
            im_name=Path(tmp_data.filename).parts[-1]
            #Remove the file extension
            prefix,extension=Path(im_name).stem,Path(im_name).suffix
            #Create new image channel i in each iteration
            nifti_col = nib.Nifti1Image(tmp_data[:,:,i], affine=np.eye(4))
            #Create the image path for this iteration
            tmp_image=prefix+"_Unregistered"+str(i)+extension
            #Save the nifti image
            print("Saving a temporary image for channel "+str(i)+"...")
            nib.save(nifti_col,str(tmp_image))
            #Now load the image and run transformix on that channel in the shell
            print("Running Transformix for channel "+str(i)+"...")
            #Creat a new file for your transformix results
            transformix_path = Path(os.path.join(str(output_dir),str(prefix)+"_Transformix_Registered"+str(i)))
            transformix_path.mkdir()
            os.system("transformix -in " +str(tmp_image)+ " -out "+str(transformix_path)+" -tp "+str(parameter_file))
            print("Finished Transforming Channel "+str(i))
            #add filenames to the list
            filenames_channels.append(os.path.join(str(transformix_path),"result.nii"))
        #Check to see if we are concatenating images
        if conc is True:
            tmp_nii = nib.concat_images(filenames_channels)
            #Create a path and save the image
            conc_path = Path(os.path.join(str(output_dir),str(prefix)+"_Transformix_Registered"))
            conc_path.mkdir()
            os.chdir(conc_path)
            nib.save(tmp_nii,"result.nii")

            #Create a return path
            ret_path = conc_path

        #Set working directory back to its original
        os.chdir(home_dir)
    else:
        print("Single channel image detected...")
        print("Running Transformix...")
        #Send the command to the shell to run transformix
        os.system("transformix -in " +str(input_img)+ " -out "+str(output_dir)+" -tp "+str(parameter_file))
        trans_stop = time.time()
        print('Finished transforming\n'+'Transformix Computation Time: '+str(trans_stop-trans_start)+' sec.')

        #Create a return path
        ret_path = output_dir

    return ret_path
