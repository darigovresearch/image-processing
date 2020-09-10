import os
import glob
import logging
import settings
import warnings
import numpy as np
import matplotlib.pyplot as plt

# from scipy.misc import imread
from osgeo import gdal
from osgeo.gdalconst import *


class Processing:
    """
    """

    def __init__(self):
        pass

    def stacking(self, safe_folder, output_path, file_pattern):
        pass
        # """
        # :param safe_folder:
        # :param output_path:
        # :param file_pattern:
        # :return:
        # usage: stacking('/data/ITEM_IMAGE.SAFE/', '/data/stack/', "_10m.jp2")
        # """
        # if os.path.isdir(safe_folder):
        #     safe_item = safe_folder.split(".")[0]
        #     list_images = glob.glob(safe_folder + "/**/*" + file_pattern, recursive=True)
        #
        #     if len(list_images) != 0:
        #         if len(list_images) == len(settings.PARAMS['S2']['bands']):
        #             logging.info(">> Stacking scene {}...".format(safe_folder))
        #
        #             output_path_aux = os.path.join(output_path, safe_item + "_" + "stk.tif")
        #
        #             command = "gdal_merge.py -of gtiff -ot float32 -co COMPRESS=NONE -co BIGTIFF=IF_NEEDED " \
        #                       "-separate -n 0 -a_nodata 0 " + " -o " + output_path_aux + " " + " ".join(list_images)
        #
        #             os.system(command)
        #     else:
        #         logging.warning(
        #             ">>>> The path {} is either empty, no .zip or SAFE formats available!".format(safe_folder))
