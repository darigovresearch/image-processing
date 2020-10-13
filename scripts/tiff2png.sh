#!/bin/bash
# Usage: ./tiff2png PATH_TO_TIFF_FOLDER
# Source: https://stackoverflow.com/questions/48944819/image-open-gives-error-cannot-identify-image-file
#         https://gis.stackexchange.com/questions/255336/convert-tif-to-png-without-normalizing-alpha
#         https://gis.stackexchange.com/questions/246934/translating-geotiff-to-16-bit-png-with-gdal
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