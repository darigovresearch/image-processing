import os
import imageio
import logging
import settings


class Processing:
    """
    """

    def __init__(self):
        pass

    def reduce_depth(self, path_with_tiffs, output_path_to_new_images):
        """
        """
        if os.path.isfile(path_with_tiffs):
            logging.info(">>>> The path {} is actually a file. A directory is expected!")
            return

        list_tiff_files = os.listdir(path_with_tiffs)
        if len(list_tiff_files) == 0:
            logging.info(">>>> The path {} with TIFF files, are empty!")
            return

        for item in list_tiff_files:
            if item.endswith(settings.VALID_RASTER_EXTENSION):
                image = imageio.imread(os.path.join(path_with_tiffs, item))

                if image.dtype == 'uint16':
                    logging.info(">>>> Converting tiff {} in 8 bits PNG...".format(image.dtype))

                    image = image / 256
                    image = image.astype('uint8')
                    image = (image >> 8).astype('uint8')
                    imageio.imwrite(os.path.join(output_path_to_new_images, item), image)
                else:
                    logging.info(">>>>>> Image depth {} does not match for conversion!".format(image.dtype))
