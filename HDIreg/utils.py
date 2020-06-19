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






#
