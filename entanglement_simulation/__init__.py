from pathlib import Path

# Specify the root and other directories of the project.
ROOT_DIR = Path(__file__).parent
DATA_DIR = Path(__file__).parent / "data"
EXPERIMENT_DIR = Path(__file__).parent.parent / "experiments/"
WATER_DATA_FILE_PATH_A = DATA_DIR / "water_data_case_a.json"
WATER_DATA_FILE_PATH_B = DATA_DIR / "water_data_case_b.json"
WATER_DATA_FILE_PATH_C = DATA_DIR / "water_data_case_c.json"
