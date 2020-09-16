# Weights WV-3: https://www.researchgate.net/publication/318702526_Influence_of_the_weights_in_IHS_and_Brovey_methods_for_pan-sharpening_WorldView-3_satellite_images
# Source: https://gdal.org/programs/gdal_pansharpen.html
#!/bin/bash

BASE=PATH_TO_WV3_IMAGES
PATH_MULT=SUBPATH_TO_WV3_MULT_IMAGES
PATH_PAN=SUBPATH_TO_WV3_PAN_IMAGES
PATH_RESULT=PATH_TO_OUTPUT

for mult_image in $BASE$PATH_MULT/*.TIF; do
    filename=$(basename $mult_image)
    pan_filename=$(echo "$filename" | sed -e 's/M3DS/P3DS/i')
    pan_image=$BASE$PATH_PAN/$pan_filename
    result_image=$PATH_RESULT/$filename
    gdal_pansharpen.py -nodata 0 -w 0.005 -w 0.142 -w 0.209 -w 0.144 -w 0.234 -w 0.234 -w 0.157 -w 0.116 $pan_image $mult_image $result_image
done
