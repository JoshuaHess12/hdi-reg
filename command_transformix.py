#Command line implementation for HDIreg module using command line input
#Developer: Joshua M. Hess, BSc
#Developed at the Vaccine & Immunotherapy Center, Mass. General Hospital

#Import custom modules
import parse_input
from HDIreg import transformix

#Parse the command line arguments
args = parse_input.ParseCommandTransformix()

#Run the elastix registration function
transformix.Transformix(**args)
