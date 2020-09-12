from decouple import config

USER_SENTINEL_HUB = config('USER_SENTINEL_HUB', default='USER_SENTINEL_HUB')
PASS_SENTINEL_HUB = config('PASS_SENTINEL_HUB', default='PASS_SENTINEL_HUB')

VALID_RASTER_EXTENSION = (".jpg", ".png", ".tif", ".tiff", ".JPG", ".PNG", ".TIF", ".TIFF")
VALID_VECTOR_EXTENSION = ".shp"

CLASS_NAME = 'class'
CLASSES = {
    "nut": [102, 153, 0],
    "palm": [153, 255, 153]
}


