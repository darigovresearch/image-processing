from decouple import config

USER_SENTINEL_HUB = config('USER_SENTINEL_HUB', default='USER_SENTINEL_HUB')

VALID_RASTER_EXTENSION = (".jpg", ".png", ".tif", ".tiff", ".JPG", ".PNG", ".TIF", ".TIFF")
VALID_VECTOR_EXTENSION = ".shp"

ALL_BANDS = True
RASTER_TILES_COMPOSITION = ['5', '3', '2']
CLASS_NAME = 'class'
CLASSES = {
    'color': {
        "other": [0, 0, 0],
        "nut": [102, 153, 0],
        "palm": [153, 255, 153]
    },
    'type': {
        "other": 0,
        "nut": 1,
        "palm": 2
    }
}


