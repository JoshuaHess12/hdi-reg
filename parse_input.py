#Functions for parsing command line arguments elastix for HDIreg
#Developer: Joshua M. Hess, BSc
#Developed at the Vaccine & Immunotherapy Center, Mass. General Hospital

#Import external modules
import argparse


def ParseCommandElastix():
   """Function for parsing command line arguments for input to elastix
   """

#if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('--fixed')
   parser.add_argument('--moving')
   parser.add_argument('--out_dir')
   parser.add_argument('--p', nargs='*')
   parser.add_argument('--fp')
   parser.add_argument('--mp')
   parser.add_argument('--fMask')
   args = parser.parse_args()
   #Create a dictionary object to pass to the next function
   dict = {'fixed': args.fixed, 'moving': args.moving, 'out_dir': args.out_dir,\
   'p': args.p, 'fp': args.fp, 'mp': args.mp, 'fMask': args.fMask}
   #Print the dictionary object
   print(dict)
   #Return the dictionary
   return dict

def ParseCommandTransformix():
   """Function for parsing command line arguments for input to transformix
   """

#if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('--in_im')
   parser.add_argument('--out_dir')
   parser.add_argument('--tps', nargs='*')
   parser.add_argument('--in_target_size')
   parser.add_argument('--crops')
   args = parser.parse_args()
   #Create a dictionary object to pass to the next function
   dict = {'in_im': args.in_im, 'out_dir': args.out_dir, 'tps': args.tps,\
   'in_target_size': args.in_target_size, 'crops': args.crops}
   #Print the dictionary object
   print(dict)
   #Return the dictionary
   return dict
