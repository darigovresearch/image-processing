# Script for Pan-Sharpening WorldView 2 and WorldView-3 images, according to IHS and Brovey methods
# Source:
#   - https://gdal.org/programs/gdal_pansharpen.html
#
# Weights WV-2
# Source:
#   -
#
# Weights WV-3
# Source:
#   - https://www.researchgate.net/publication/318702526_Influence_of_the_weights_in_IHS_and_Brovey_methods_for_pan-sharpening_WorldView-3_satellite_images
#
# Usage:
#   - ./pan-sharp PATH_TO_WV3_IMAGES SUBPATH_TO_MULT_IMAGES SUBPATH_TO_PAN_IMAGES PATH_TO_OUTPUT
#
# Example:
#   - ./pan-sharp /media/rodolfo/data/bioverse/images/kayapo/original-images/wv2/bioverse_wv2_1_013505213_10_0/
#                 013505213010_01_003/013505213010_01/013505213010_01_P001_MUL/
#                 013505213010_01_003/013505213010_01/013505213010_01_P001_PAN/
#                 /media/rodolfo/data/bioverse/images/kayapo/pan-sharpening/wv2/pan-sharp-campaign-1/
#!/bin/bash

PATH_TO_WV3_IMAGES=$1
SUBPATH_TO_MULT_IMAGES=$2
SUBPATH_TO_PAN_IMAGES=$3
PATH_TO_OUTPUT=$4

BASE=$PATH_TO_WV3_IMAGES
PATH_MULT=$SUBPATH_TO_MULT_IMAGES
PATH_PAN=$SUBPATH_TO_PAN_IMAGES
PATH_RESULT=$PATH_TO_OUTPUT

WV2_W='-w 0.095 -w 0.7 -w 0.35 -w 1.0 -w 1.0 -w 1.0 -w 1.0 -w 1.0'
WV3_W='-w 0.005 -w 0.142 -w 0.209 -w 0.144 -w 0.234 -w 0.234 -w 0.157 -w 0.116'

for mult_image in $BASE$PATH_MULT/*.TIF; do
    filename=$(basename $mult_image)
    pan_filename=$(echo "$filename" | sed -e 's/M3DS/P3DS/i')
    pan_image=$BASE$PATH_PAN/$pan_filename
    result_image=$PATH_RESULT/$filename
    gdal_pansharpen.py -nodata 0 $WV2_W $pan_image $mult_image $result_image
done
