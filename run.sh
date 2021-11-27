#!/bin/bash
# A script to generate training samples through raster (tiff) and vector (shapefile) on demand
# usage: ./run.sh PATH_TO_FULL_IMAGES
#                 PATH_TO_SAVE_RASTER_TILES
#                 DIMENSION_OF_THE_TILES
#                 PATH_TO_FULL_SHAPEFILES
#                 PATH_TO_SAVE_VECTOR_TILES
#                 PATH_TO_PNG_ANNOTATION_IMAGES

RASTER_PATH=$1
RASTER_TILE_OUTPUT=$2
SQUARED_DIMENSION=$3
VECTOR_PATH=$4
VECTOR_TILE_OUTPUT=$5
OUTPUT_ANNOTATION=$6


for entry in "$RASTER_PATH"*
do
  if [ -f "$entry" ];then
    filename=$(basename -- "$entry")
    extension="${filename##*.}"
    name="${filename%.*}"
    shp_reference="$VECTOR_PATH$name.shp"

      python main.py -procedure tiling_raster -image "$entry" -output "$RASTER_TILE_OUTPUT" -tile_width "$SQUARED_DIMENSION" -tile_height "$SQUARED_DIMENSION" -verbose True &&
      python main.py -procedure tiling_vector -image_tiles "$RASTER_TILE_OUTPUT" -output "$VECTOR_TILE_OUTPUT" -shapefile_reference "$shp_reference" -verbose True
  fi
done

python main.py -procedure shp2png -image "$RASTER_TILE_OUTPUT" -shapefile_folder "$VECTOR_TILE_OUTPUT" -output "$OUTPUT_ANNOTATION" -tile_width "$SQUARED_DIMENSION" -tile_height "$SQUARED_DIMENSION" -verbose True
