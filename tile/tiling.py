import os
import gdal
import logging
import shapefile
import geopandas as gp
import glob
import settings

from shapely.geometry import Polygon
from PIL import Image, ImageDraw

logging.getLogger('shapely.geos').setLevel(logging.CRITICAL)


class Tiling:
    """ Command-line routine to tile images and shapefiles according to desired width and heights """

    def __init__(self):
        pass

    # TODO: refactor slice_array
    def slice_array(self, array, positions):
        """
        :param array:
        :param positions:
        :return:
        """
        new_arrays = []
        positions.append(len(array) - 1)

        for i in range(len(positions) - 1):
            new_arrays.append(array[positions[i]:positions[i + 1]])

        return new_arrays

    def shp2png(self, raster_folder, shapefile_folder, output_folder, width, height, classes, is_grayscale):
        """
        Source: https://github.com/GeospatialPython/geospatialpython/blob/master/shp2img.py
        Example of classes variable:
        classes = {
                "def": [255, 255, 0],
                "water": [102, 204, 255],
                "cloud": [255, 255, 255],
                "shadow": [128, 128, 128]
            }
        :param raster_folder:
        :param shapefile_folder:
        :param output_folder:
        :param width:
        :param height:
        :param classes:
        :param is_grayscale: if True, the label images is built with CLASSES ID instead of CLASSES COLOR
        :return:
        """
        files = os.listdir(shapefile_folder)
        shp_list = [file for file in files if file.endswith(settings.VALID_VECTOR_EXTENSION)]

        for shape in shp_list:
            name, file_extension = os.path.splitext(shape)
            shape_path = os.path.join(shapefile_folder, shape)
            output = os.path.join(output_folder, name + ".png")
            raster = os.path.join(raster_folder, name + ".TIF")

            if os.path.isfile(raster):
                tile = gdal.Open(raster)
                gt = tile.GetGeoTransform()
                cols_tile = tile.RasterXSize
                rows_tile = tile.RasterYSize
                ext = self.get_extent(gt, cols_tile, rows_tile)
            else:
                continue

            if os.path.isfile(shape_path):
                # TODO: to predict the encoding - hardcoded
                r = shapefile.Reader(shape_path, encoding='ISO8859-1')
                if not r:
                    logging.info('>>>> Error: could not open the shapefile')
                    continue
            else:
                logging.info('>>>> Error: could not open the shapefile')
                continue

            x_dist = ext[3][0] - ext[1][0]
            y_dist = ext[3][1] - ext[1][1]
            x_ratio = width / x_dist
            y_ratio = height / y_dist

            shapes = r.shapes()
            records = r.records()

            if is_grayscale is True:
                img = Image.new("L", (width, height), "black")
                classes_content = classes['type']
            else:
                img = Image.new("RGB", (width, height), "black")
                classes_content = classes['color']

            draw = ImageDraw.Draw(img)

            for i, record in enumerate(records):
                if record[1] in classes_content:
                    parts = shapes[i].parts
                    pixels = []

                    if is_grayscale is True:
                        fill_color = classes_content[record[1]]
                    else:
                        fill_color = "rgb(" + str(classes[classes_content[1]][0]) + ", " + str(
                            classes_content[record[1]][1]) + ", " + str(classes_content[record[1]][2]) + ")"

                    for x, y in shapes[i].points:
                        px = int(width - ((ext[3][0] - x) * x_ratio))
                        py = int((ext[3][1] - y) * y_ratio)
                        pixels.append((px, py))

                    if len(parts) > 1:
                        polygons_parts = self.slice_array(pixels, parts)
                        for k in range(len(polygons_parts)):
                            draw.polygon(polygons_parts[k], outline=None,
                                         fill=fill_color)
                    else:
                        draw.polygon(pixels, outline=None, fill=fill_color)
            img.save(output)

    def get_extent(self, gt, cols, rows):
        """
        Source: https://gis.stackexchange.com/questions/57834/how-to-get-raster-corner-coordinates-using-python-gdal-bindings
        :param gt:
        :param cols:
        :param rows:
        :return:
        """
        ext = []
        x_arr = [0, cols]
        y_arr = [0, rows]

        for px in x_arr:
            for py in y_arr:
                x = gt[0] + (px * gt[1]) + (py * gt[2])
                y = gt[3] + (px * gt[4]) + (py * gt[5])
                ext.append([x, y])
            y_arr.reverse()
        return ext

    def tiling_raster(self, image, output_folder, width, height):
        """
        :param image:
        :param output_folder:
        :param width:
        :param height:
        :return:
        """
        # TODO: test with endswith is not working
        if os.path.isfile(image) and image.endswith(settings.VALID_RASTER_EXTENSION):
            filename = os.path.basename(image)
            name, file_extension = os.path.splitext(filename)
            ds = gdal.Open(image)

            if ds is None:
                logging.warning(">>>>>> Could not open image file {}. Skipped!".format(image))

            stats = [ds.GetRasterBand(i + 1).GetStatistics(True, True) for i in range(ds.RasterCount)]
            vmin, vmax, vmean, vstd = zip(*stats)

            rows = ds.RasterXSize
            cols = ds.RasterYSize
            tiles_cols = cols / width
            tiles_rows = rows / height
            logging.info(">>>> Tiling image {}. {} x {} pixels. Estimated {} tiles of {} x {}..."
                         .format(image, rows, cols, round(tiles_cols * tiles_rows), width, height))

            gdal.UseExceptions()
            for i in range(0, rows, width):
                for j in range(0, cols, height):
                    try:
                        output = os.path.join(output_folder, name + "_" + str(i) + "_" + str(j) + file_extension)
                        gdal.Translate(output, ds, format='GTIFF', srcWin=[i, j, width, height],
                                       outputType=gdal.GDT_Byte, scaleParams=[[list(zip(*[vmin, vmax]))]],
                                       options=['-epo', '-eco', '-b', '5', '-b', '3', '-b', '2'])

                    except RuntimeError:
                        continue
        else:
            logging.info(">>>> Image file {} does not exist or is a invalid extension!".format(image))

    def tiling_vector(self, image_tiles_folder, shp_reference, output_folder):
        """
        :param image_tiles_folder:
        :param shp_reference:
        :param output_folder:
        :return:
        """
        if not os.path.isdir(image_tiles_folder):
            logging.warning(">>>> {} is not a folder!".format(image_tiles_folder))
            return

        if not os.path.isfile(shp_reference):
            logging.warning(">>>> {} is not a file!".format(shp_reference))
            return

        filename = os.path.basename(shp_reference)
        name, file_extension = os.path.splitext(filename)

        if file_extension.lower() not in settings.VALID_VECTOR_EXTENSION:
            logging.warning(">>>> {} not a valid extension for a vector!".format(file_extension))
            return

        list_correspondent_raster = glob.glob(os.path.join(image_tiles_folder, name + '*'))
        if len(list_correspondent_raster) == 0:
            logging.info(">>>> No raster tiles with shapefile suffix {}".format(name))
            return

        logging.info(">> Tiling vector {} respecting to the tiles extends".format(shp_reference))
        for image in list_correspondent_raster:
            filename = os.path.basename(image)
            name, ext = os.path.splitext(filename)

            if ext.lower() not in settings.VALID_RASTER_EXTENSION:
                logging.warning(">>>> {} not a valid extension for a raster!".format(ext))
                continue

            complete_path = os.path.join(image_tiles_folder, image)
            tile = gdal.Open(complete_path)

            prj = tile.GetProjection()
            gt = tile.GetGeoTransform()
            cols_tile = tile.RasterXSize
            rows_tile = tile.RasterYSize
            ext = self.get_extent(gt, cols_tile, rows_tile)

            bounds = Polygon(ext)
            baseshp = gp.read_file(shp_reference)

            # TODO: define shapefile crs from image crs - hardcoded
            # srs = osr.SpatialReference()
            # srs.ImportFromWkt(prj)
            baseshp = baseshp.to_crs(epsg=32722)

            ids = []
            classes = []
            polygons_intersecting = []
            for i in range(len(baseshp)):
                p1 = baseshp['geometry'][i]
                p2 = bounds

                if p1 is None:
                    logging.info(">>>>>> Geometry is empty! File {}".format(os.path.basename(shp_reference)))
                    continue

                if p1.is_valid is False:
                    p1 = p1.buffer(0)

                if not p1.intersection(p2).is_empty:
                    ids.append(i)
                    classes.append(baseshp[settings.CLASS_NAME][i])
                    polygons_intersecting.append(p1.intersection(p2))

            if len(polygons_intersecting) != 0:
                gdf = gp.GeoDataFrame()
                gdf.crs = baseshp.crs
                gdf['id'] = ids
                gdf['class'] = classes
                gdf['geometry'] = polygons_intersecting

                output = os.path.join(output_folder, name + ".shp")
                gdf.to_file(output, driver='ESRI Shapefile')
            else:
                os.remove(complete_path)

