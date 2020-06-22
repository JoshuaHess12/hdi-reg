#Functions for general purpose usage
#Joshua Hess
import os
from pathlib import Path
import re
import pandas as pd
import numpy as np


def SearchDir(ending = ".txt",dir=None):
    """Function for searching only in current directory for files that end with
    the specified suffix

    Returns a list of full path file names"""

    #If directory is not specified, use the working directory
    if dir is None:
        tmp = Path('..')
        dir = tmp.cwd()
    #Search the directory only for files
    full_list = []
    for file in os.listdir(dir):
        if file.endswith(ending):
            full_list.append(Path(os.path.join(dir,file)))
    #Return the list
    return full_list


def TraverseDir(ending=".txt",dir=None):
    """Function for traversing a directory to search for files that end with the
    specified suffix

    Returns a list of full path file names"""

    #If directory is not specified, use the working directory
    if dir is None:
        tmp = Path('..')
        dir = tmp.cwd()
    #Traverse the directory to search for files
    full_list = []
    for root, dirs, files in os.walk(dir):
        for f in files:
            if f.endswith(ending):
                full_list.append(Path(os.path.join(root,f)))
    #Return the list
    return full_list



def GetFinalTransformParameters(dir=None):
    """Function for parsing an elastix parameter file or elastix.log file and
    extracting a number associated with the given string parameter"""

    #If directory is not specified, use the working directory
    if dir is None:
        tmp = Path('..')
        dir = tmp.cwd()

    #Search the directory only for files
    full_list = []
    for file in os.listdir(dir):
        if "TransformParameters" in file:
            full_list.append(Path(os.path.join(dir,file)))
    #Order the list to get the last transform parameter file
    full_list.sort(key=lambda f: int(str(f).split("TransformParameters.")[1].split(".")[0]))
    #Return the list
    return full_list[-1],full_list



def ParseElastix(input,par):
    """Function for parsing an elastix parameter file or elastix.log file and
    extracting a number associated with the given string parameter"""

    #Read the transform parameters
    with open(input, 'r') as file:
        filedata = file.readlines()
    #Add each line to a list with separation
    result=[]
    for x in filedata:
        result.append(x.split('\n')[0])
    #Find the parameter (Add a space for a match)
    lines = [s for s in result if str(par+' ') in s][-1]
    number = re.findall(r"[-+]?\d*\.\d+|\d+", lines)[0]
    #Try to convert to integer, otherwise convert to float
    if number.isdigit():
        num = int(number)
    else:
        num = float(number)
    #Return the number
    return number, num



def ComposeTransforms(tps,out_dir):
    """Function for composing a list of transform parameters together from
    elastix

    tps: list of paths for parameter files to string together -- in order of composition!
    out_dir: Path to export newly generated/copied transform parameter files
    """

    #Ensure the given transform parameters are pathlib objects
    tps = [Path(tp) for tp in tps]
    #Ensure the output directory is pathlib object
    out_dir = Path(out_dir)
    #Create a list of new filenames that will be exported
    new_tps = [Path(os.path.join(str(out_dir),"TransformParameters_comp."+str(i)+".txt")) for i in range(len(tps))]

    #Extract and modify the first file in the list of transform parameters
    with open(tps[0], 'r') as file:
        #Read the file
        filedata = file.read()
        #Search for the initial transform parameter
        for l in list(filedata.split("\n")):
            #Check if inital transform string is in the line
            if "InitialTransformParametersFileName" in l:
                #Extract the inital transform parameter string
                init_trans = str(l.split(" ")[1].strip(")").strip('"'))

    #Check to ensure that the initial transform is no initial transform
    if not init_trans == 'NoInitialTransform':
        #Then replace the initial transform in the file with no inital transform
        filedata = filedata.replace(init_trans, 'NoInitialTransform')
    
    #Write out the new data to the new transform parameter filename
    with open(new_tps[0], 'w') as file:
        #Write the new file
        file.write(filedata)

    #Remove the filedata for now
    filedata = None

    #Iterate through all other files and change inital transforms
    for t in range(1,len(tps[1:])+1):
        #Extract and modify the first file in the list of transform parameters
        with open(tps[t], 'r') as f:
            #Read the file
            filedata = f.read()
            #Search for the initial transform parameter
            for l in list(filedata.split("\n")):
                #Check if inital transform string is in the line
                if "InitialTransformParametersFileName" in l:
                    #Extract the inital transform parameter string
                    init_trans = l.split(" ")[1].strip(")").strip('"')

        #Then replace the initial transform in the file with the previous transform
        filedata = filedata.replace(init_trans, str(new_tps[t-1]))

        #Write out the new data to the new transform parameter filename
        with open(new_tps[t], 'w') as file:
            #Write the new file
            file.write(filedata)

    #Remove the filedata for now
    filedata = None

    #Return the list of new parameter files
    return new_tps

#
