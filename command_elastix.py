#Command line implementation for HDIreg module using command line input
#Developer: Joshua M. Hess, BSc
#Developed at the Vaccine & Immunotherapy Center, Mass. General Hospital

#Import custom modules
import parse_input
import yaml_elastix

#Parse the command line arguments
args = parse_input.ParseCommandElastixYAML()

#Run the elastix registration function
yaml_elastix.RunElastixYAML(**args)
