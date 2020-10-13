from decouple import config

USER_SENTINEL_HUB = config('USER_SENTINEL_HUB', default='USER_SENTINEL_HUB')

VALID_RASTER_EXTENSION = (".jpg", ".png", ".tif", ".tiff", ".JPG", ".PNG", ".TIF", ".TIFF")
VALID_VECTOR_EXTENSION = ".shp"

CLASS_NAME = 'class'
CLASSES = {
    'color': {
        "nut": [102, 153, 0],
        "palm": [153, 255, 153]
    },
    'type': {
        "nut": 1,
        "palm": 2
    }
}


