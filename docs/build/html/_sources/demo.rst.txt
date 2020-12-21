******************
Demo and Examples
******************

Examples
===================

Running the raster tilling
---------------------------
The raster tiling consists in crop the full image in small peaces in order to get a required dimension for most of the supervised classifiers.

Here, the procedure demands 6 arguments, which are the procedure to be executed (`-procedure`), the full image path (TIFF format - `-image`), the output to the tiles (`-output`), the width dimension of the tiles (`-tile_width`), the height dimension of the tiles (`-tile_height`), and a boolean verbose outcomes (`-verbose`).

.. code-block:: python

    python main.py -procedure tiling_raster
                   -image PATH_TO_FULL_IMAGE_IN_TIFF_FORMAT
                   -output PATH_TO_OUTPUT_RASTER_TILES
                   -tile_width DIMESION_OF_TILES
                   -tile_height DIMESION_OF_TILES
                   -verbose BOOLEAN

**In Linux, it should be run in main folder**

Running the vector tilling
---------------------------

The vector tiling consists in crop the full shapefile in small peaces according to the raster tiles extends processed before. The procedure saves a tiled shapefile if the full shapefile intersect a raster tile. If it does not intersect, the raster tile is then deleted (in order to save space).

Here, the procedure demands 6 arguments, which are the procedure to be executed (`-procedure`), the full shapefile path (SHP format - `-image_tiles`), the output to the tiles (`-output`), the shapefile reference (`-shapefile_reference`), and a boolean verbose outcomes (`-verbose`).

.. code-block:: python

    python main.py -procedure tiling_vector
                   -image_tiles PATH_TO_OUTPUT_RASTER_TILES
                   -output PATH_TO_OUTPUT_VECTOR_TILES
                   -shapefile_reference PATH_TO_REFERENCE_SHAPEFILES
                   -verbose BOOLEAN

**In Linux, it should be run in main folder**

Running the SHP to PNG conversion
---------------------------------

The vector tiling consists in crop the full shapefile in small peaces according to the raster tiles extends processed before. The procedure saves a tiled shapefile if the full shapefile intersect a raster tile. If it does not intersect, the raster tile is then deleted (in order to save space).

Here, the procedure demands 6 arguments, which are the procedure to be executed (`-procedure`), the shapefile tiles path (`-shapefile_folder`), the output to the final annotation images (`-output`), the width dimension of the tiles (`-tile_width`), the height dimension of the tiles (`-tile_height`), and a boolean verbose outcomes (`-verbose`).

.. code-block:: python

    python main.py -procedure shp2png
                   -shapefile_folder PATH_TO_VECTOR_TILES
                   -output PATH_TO_SAVE_ANNOTATION_IMAGES
                   -tile_width DIMESION_OF_TILES
                   -tile_height DIMESION_OF_TILES
                   -verbose BOOLEAN

**In Linux, it should be run in main folder**

Split the training and validation datasets
------------------------------------------
On going...

.. code-block:: python

    python main.py -procedure split_samples
                   -training_folder COMPLETE_PATH_TO_TRAINING_FOLDER/
                   -validation_folder COMPLETE_PATH_TO_VALIDATION_FOLDER/
                   -percentage PERCENT_DESTINATION_FOR_VALIDATION_IMAGES/
                   -verbose BOOLEAN

Convert the geographic format, to DL known format
-------------------------------------------------
On going...

.. code-block:: bash

    ./tiff2png.sh PATH_TO_TIFF_FOLDER

**In Linux, it should be run in the `scripts` folder**

Keras/Pillow format file required
---------------------------------

Some image formats do not work well over the `Keras framework <https://keras.io/>`_, such as, TIFF format. For that reason, the tiles generated in `tiling_vector` can then be converted in PNG format using `gdal_translate` `More details <https://gdal.org/programs/gdal_translate.html>`_, finally get the final version of the Deep Learning input. The shellscript `tiff2png` is an auxiliary file to translate all tiff repository in png format:

.. code-block:: bash

    for entry in $1*
    do
      if [ -f "$entry" ];then
        dir=$(dirname "$entry")"/"
        filename=$(basename -- "$entry")
        extension="${filename##*.}"
        name="${filename%.*}"
        gdal_translate -of PNG -B 1 -B 2 -B 3 $dir$filename $dir$name".PNG"
        rm $entry
        rm $dir$name".PNG.aux.xml"
      fi
    done

just under `scripts/` folder, run:

.. code-block:: bash

    ./tiff2png PATH_TO_TIFF_FOLDER

Bash for sequential processing `run.sh`
---------------------------------------

Compiling the three procedures in one, the shellscript `run.sh`, in `/scripts` can be then apply for multiple images and shapefiles, generating a consistent amount of samples. So, this file simply summary all processing until the final pair of training samples, which is the pair of image and its correspondent reference (annotation image). So, the only thing needed are the full images (preference in `.tiff` format), and its full correspondent shapefiles (ESRI Shapefile format - `.shp` extension).

.. code-block:: bash

    RASTER_PATH=$1
    RASTER_TILE_OUTPUT=$2
    SQUARED_DIMENSION=$3
    VECTOR_PATH=$4
    VECTOR_TILE_OUTPUT=$5
    OUTPUT_ANNOTATION=$6

    for entry in "$RASTER_PATH"*
    do
      if [ -f "$entry" ];then
        filename=$(basename $entry)

        python main.py -procedure tiling_raster -image "$entry" -output "$RASTER_TILE_OUTPUT" -tile_width "$SQUARED_DIMENSION" -tile_height "$SQUARED_DIMENSION" -verbose True &&
        python main.py -procedure tiling_vector -image_tiles "$RASTER_TILE_OUTPUT" -output "$VECTOR_TILE_OUTPUT" -shapefile_reference "$VECTOR_PATH" -verbose True
      fi
    done

    python main.py -procedure shp2png -image "$RASTER_TILE_OUTPUT" -shapefile_folder "$VECTOR_TILE_OUTPUT" -output "$OUTPUT_ANNOTATION" -tile_width "$SQUARED_DIMENSION" -tile_height "$SQUARED_DIMENSION" -verbose True



