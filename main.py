import os
import sys
import logging
import argparse
import settings

from coloredlogs import ColoredFormatter
from tile import tiling
from utils import utils

os.environ['GDAL_PAM_ENABLED'] = 'NO'


def main(arguments):
    """
    Method to start the workflow of image processing

    :param arguments: the arguments passed by the user. Determines which procedure will be performed
    """
    if arguments.procedure is not None:
        if arguments.procedure == 'tiling_raster':
            if (arguments.image is not None) and (arguments.output is not None) \
                    and (arguments.width is not None) and (arguments.height is not None):
                tiling.Tiling().tiling_raster(arguments.image, arguments.output, arguments.width, arguments.height,
                                              True)
            else:
                logging.error(">> One of arguments (image_folder, output_folder, weight, height) are incorrect or "
                              "empty. Try it again!")
                raise RuntimeError
        elif arguments.procedure == 'tiling_vector':
            if (arguments.image_tiles is not None) and (arguments.shapefile_reference is not None) and \
                    (arguments.output is not None):
                tiling.Tiling().tiling_vector(arguments.image_tiles, arguments.shapefile_reference, arguments.output)
            else:
                logging.error(">> One of arguments (image_tiles, shapefile_reference, output_folder) are incorrect or "
                              "empty. Try it again!")
                raise RuntimeError
        elif arguments.procedure == 'shp2png':
            if (arguments.image is not None) and (arguments.shapefile_folder is not None) and \
                    (arguments.output is not None) and (arguments.width is not None) and (arguments.height is not None):
                tiling.Tiling().shp2png(arguments.image, arguments.shapefile_folder, arguments.output,
                                        arguments.width, arguments.height, settings.CLASSES, label_type='class_id')
            else:
                logging.error(">> One of arguments (image_folder, shapefile_reference, output_folder) are incorrect or "
                              "empty. Try it again!")
                raise RuntimeError

        elif arguments.procedure == 'split_samples':
            if (arguments.training_folder is not None) and (arguments.validation_folder is not None) and \
                    (arguments.percentage is not None):
                utils.Utils().split_samples(arguments.training_folder, arguments.validation_folder,
                                            arguments.percentage)
            else:
                logging.error(">> One of arguments (training_folder, validation_folder, percentage) are incorrect or "
                              "empty. Try it again!")
                raise RuntimeError
        else:
            logging.error(">> Procedure option not found. Try it again!")
            raise RuntimeError


if __name__ == '__main__':
    """ 
    Command-line routine for supervised samples preparation. This set of commands combine the tiling of remote
     sensing datasets and geographic vector layers (shapefile), in order to model the inputs for most deep learning 
     frameworks available. It actually convert massive images in small patches with its respective references 
     (i.e. annotation images)
     
    Usage:
        > python main.py -procedure tiling_raster 
                       -image /PATH/FILE.TIF 
                       -output PATH_TO_OUTPUT_RASTER_TILES/
                       -tile_width INT -tile_height INT 
                       -verbose BOOLEAN
        > python main.py -procedure tiling_vector
                       -image_tiles PATH_TO_RASTER_TILES/
                       -output PATH_TO_OUTPUT_VECTOR_TILES/
                       -shapefile_reference /PATH/REFERENCE.SHP
                       -verbose BOOLEAN     
        > python main.py -procedure shp2png
                       -image PATH_TO_RASTER_TILES/
                       -shapefile_folder PATH_TO_VECTOR_TILES/
                       -output PATH_TO_OUTPUT_PNG_TILES/
                       -tile_width INT -tile_height INT 
                       -verbose BOOLEAN
        > python main.py -procedure split_samples
                       -training_folder COMPLETE_PATH_TO_TRAINING_FOLDER/
                       -validation_folder COMPLETE_PATH_TO_VALIDATION_FOLDER/                       
                       -percentage PERCENT_DESTINATION_FOR_VALIDATION_IMAGES
                       -verbose BOOLEAN
    """
    parser = argparse.ArgumentParser(description='Prepare input files for supervised neural network procedures')

    parser.add_argument('-procedure', action="store", dest='procedure', help='Procedure to be performed. Options: '
                                                                             'tiling_vector, tiling_raster, '
                                                                             'shp2png, split_samples')
    parser.add_argument('-image', action="store", dest='image', help='Images folder: the complete path to the images '
                                                                     'to be tiled')
    parser.add_argument('-image_tiles', action="store", dest='image_tiles', help='Images tiles: the complete path to '
                                                                                 'the raster tiles')
    parser.add_argument('-output', action="store", dest='output', help='Output folder: the complete path to output')
    parser.add_argument('-shapefile_reference', action="store", dest='shapefile_reference',
                        help='ESRI Shapefile to be used as reference to generate the respective annotation for image '
                             'tiles. The image_folder argument, in this case, has to be the image tiles folder')
    parser.add_argument('-shapefile_folder', action="store", dest='shapefile_folder', help='Shapefile tiles folder: '
                                                                                           'the complete path to '
                                                                                           'the vector tiles')
    parser.add_argument('-tile_width', action="store", dest='width', type=int, help='Integer tile width')
    parser.add_argument('-tile_height', action="store", dest='height', type=int, help='Integer tile height')
    parser.add_argument('-training_folder', action="store", dest='training_folder', help='The training folder with '
                                                                                         'image/ and label/ datasets')
    parser.add_argument('-validation_folder', action="store", dest='validation_folder', help='The validation folder '
                                                                                             'with image/ and label/ '
                                                                                             'folders. The '
                                                                                             'split_samples procedure '
                                                                                             'will cut a percentage of '
                                                                                             'training imagens and will'
                                                                                             ' place it here')
    parser.add_argument('-percentage', action="store", dest='percentage', help='Integer [0-100] denoting the amount of '
                                                                               'training samples to be used for '
                                                                               'validation')
    parser.add_argument('-verbose', action="store", dest='verbose', help='Boolean (True or False) '
                                                                         'for printing log or not')

    args = parser.parse_args()

    if eval(args.verbose):
        log = logging.getLogger('')

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        cf = ColoredFormatter("[%(asctime)s] {%(filename)-15s:%(lineno)-4s} %(levelname)-5s: %(message)s ")
        ch.setFormatter(cf)
        log.addHandler(ch)

        fh = logging.FileHandler('logging.log')
        fh.setLevel(logging.INFO)
        ff = logging.Formatter("[%(asctime)s] {%(filename)-15s:%(lineno)-4s} %(levelname)-5s: %(message)s ",
                               datefmt='%Y.%m.%d %H:%M:%S')
        fh.setFormatter(ff)
        log.addHandler(fh)

        log.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    main(args)
