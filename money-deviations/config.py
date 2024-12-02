# get the directory path of the file
import os

root_path = os.path.dirname(__file__)

TEMP_PATH = f"{root_path}/temp/"
DATA_NASA_PATH = f"{root_path}/temp/nasa/"
IMAGE_PATH = f"{root_path}/temp/images/"


PLANT_NAME = {
    "EPFV": "Solar 1",  # EL PASO
    "3IRX": "Solar 2",  # PORTON DEL SOL ##Cartagena
    "3HF5": "Solar 3",  # FUNDACION ##Meta
    "MATA": "Solar 4",  # La mata  ##Valledupar
    "3IZ6": "Solar 5",  # PARQUE SOLAR LA UNION
    "3DDT": "Solar 6",  # LATAM SOLAR LA LOMA
    "TPUY": "Solar 7",  # TEPUY ## Caldas
}
