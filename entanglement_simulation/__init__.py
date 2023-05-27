from pathlib import Path

# Specify the root and other directories of the project.
ROOT_DIR = Path(__file__).parent
DATA_DIR = Path(__file__).parent / "data"
EXPERIMENT_DIR = Path(__file__).parent.parent / "experiments/"
WATER_DATA_FILE_PATH = DATA_DIR / "water_data.json"
