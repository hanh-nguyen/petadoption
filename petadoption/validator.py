import os
import pandas as pd
import logging

# Logging setup
logging.basicConfig(format='%(levelname)s: %(module)s: %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger('__name__')

# Define Global Variables
SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '../exploration/data'))


class Validator(object):
    """
        Class that can be used to validate animal inputs
        
        Parameters:
            supported_colors (dict): Contains all supported colors
    """
    
    def __init__(self):
        self.supported_colors = self.get_supported_colors()
    
    def __repr__(self):
        return "ValidatorObject()"
    
    
    def get_supported_colors(self):
        """
            Method to store the supported colors
            
            Returns: supported_colors (dict): Color name: Color ID
        """
        
        color_labels_file = os.path.join(DATA_DIR, 'color_labels.csv')
        color_labels_df = pd.read_csv(color_labels_file, index_col=1)
        color_labels_df.index = color_labels_df.index.str.lower()
        supported_colors = color_labels_df.to_dict()['ColorID']
        
        return supported_colors
        
        
    def eval_colors(self, colors):
        """
            Method to evaluate whether a color is supported by the model
            
            Inputs: colors (list): List of color names
            Returns: valid_colors (list): List of valid colors from input list
        """
        
        valid_colors = []
        for color in colors:
            if color.lower() in self.supported_colors:
                valid_colors.append(color.lower())
            else:
                LOGGER.warning("Input color '{}' is not supported, so will not"
                               " use it in the evaluation".format(color))
        if len(valid_colors) > 3:
            valid_colors = valid_colors[:3]
            LOGGER.warning("More than 3 input colors given, so using the first "
                        "3 colors specified: {}".format(valid_colors))
        
        return valid_colors