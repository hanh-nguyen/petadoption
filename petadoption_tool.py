import sys
import os
import re
from argparse import ArgumentParser, RawTextHelpFormatter
import logging
import pandas as pd
import petadoption


# Logging setup for the script
logging.basicConfig(format='%(levelname)s: %(module)s: %(message)s',
                     level=logging.INFO)
LOGGER = logging.getLogger('__name__')


# Define Global Variables
SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, 'exploration/data'))

def build_parser():
    """
        Function to build the argument parser for the script

        Returns: a parser object
    """
    
    # Set up the help page formatting
    formatter = lambda prog: RawTextHelpFormatter(prog, max_help_position=50)
    parser = ArgumentParser(description="Tool to estimate adoption time",
        formatter_class=formatter)
    sp = parser.add_subparsers()
    
    # Options when testing for a single cat
    sp_cat = sp.add_parser('cat', help='Predict adoption time for a cat')
    sp_cat.add_argument('-c', '--colors', required=True, type=str, default='',
                        help="Comma- or space-separated list of colors")
    sp_cat.add_argument('-b', '--breeds', required=False, type=str,
                        default='Domestic', help="Comma- or space-separated "
                        "list of breeds")
    
    # Options when testing for a single dog
    sp_dog = sp.add_parser('dog', help='Predict adoption time for a dog')
    sp_dog.add_argument('-c', '--colors', required=True, type=str, default='',
                        help="Comma- or space-separated list of colors")
    sp_dog.add_argument('-b', '--breeds', required=False, type=str,
                        default='Mixed', help="Comma- or space-separated "
                        "list of breeds")
    
    # Options when using an input file
    sp_file = sp.add_parser('file', help='Predict adoption time for a list of' 
                            ' animals in a CSV file')
    sp_file.add_argument('filename', type=str, default='',
                         help="Name of the CSV input file")
    
    return parser


def validate_args(parser):
    """
        Function to validate command line arguments
    """
    
    if len(sys.argv) < 2:
        LOGGER.error('Must specify "cat", "dog", or "file"')
        print(parser.print_help())
        sys.exit()


def eval_breeds(species, in_breeds):
    """
        Function to evaluate the breed(s) of a given animal
        
        Inputs: in_breeds (list): List of breed names
        Returns: out_breeds (list): List of valid breed names for evaluation
    """
    
    breed_labels_file = os.path.join(DATA_DIR, 'breed_labels.csv')
    breed_labels_df = pd.read_csv(breed_labels_file, index_col = 2)
    breed_labels_df.index = breed_labels_df.index.str.lower()
    out_breeds = []
    
    # Handle Dog Breeds
    if species == 'dog':
        supported_breeds = (breed_labels_df.loc[breed_labels_df['Type'] == 1, 
                                                'BreedID'].to_dict())
        mixed_breed_list = ['mutt', 'unknown']
        for breed in in_breeds:
            if 'mixed' in breed:
                out_breeds.append('mixed')
            elif breed in mixed_breed_list:
                out_breeds.append('mixed')
            elif breed in supported_breeds:
                out_breeds.append(breed)
            else:
                LOGGER.warning("Input breed {} is not supported, so will "
                               "use 'mixed' as the breed".format(breed))
                out_breeds.append('mixed')

    # Handle Cat Breeds
    else:
        supported_breeds = (breed_labels_df.loc[breed_labels_df['Type'] == 2,
                                   'BreedID'].to_dict())
        domestic_breed_list = ['unknown']
        for breed in in_breeds:
            if 'domestic' in breed:
                out_breeds.append('domestic')
            elif breed in domestic_breed_list:
                out_breeds.append('domestic')
            elif breed in supported_breeds:
                out_breeds.append(breed)
            else:
                LOGGER.warning("Input breed {} is not supported, so will "
                               "use 'domestic' as the breed".format(breed))
                out_breeds.append('domestic')
                
    if len(out_breeds) > 2:
        out_breeds = out_breeds[:2]
        LOGGER.warning("More than 2 input breeds given, so using the first "
                       "2 breeds specified: {}".format(out_breeds))
    
    return out_breeds
    

def main():
    """
        Main function, contains the set of steps to run for user input
    """
    
    parser = build_parser()
    validate_args(parser)
    args = parser.parse_args()
    species = sys.argv[1]
    validator = petadoption.validator.Validator()
    
    # Handle cases where the script is run to evaluate a single animal
    if species == 'cat' or species == 'dog':
        colors = [ c.lower() for c in re.split(',|, | ', args.colors) ]
        colors = validator.eval_colors(colors)
        if len(colors) == 0:
                LOGGER.error("None of the colors provided is supported, so could "
                        "not complete evaluation")
                sys.exit()
        
        breeds = [ b.lower() for b in re.split(',|, | ', args.breeds) ]
        breeds = eval_breeds(species, breeds)
        
        print("Evaluating a {} with colors {} and breeds {}".format(species,
            colors, breeds))


if __name__ == '__main__':
    main()
    