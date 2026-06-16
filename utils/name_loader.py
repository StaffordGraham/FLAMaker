from pathlib import Path
import pickle

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

with open(DATA_DIR / "boy_names_set.pkl", "rb") as f:
    boy_names = pickle.load(f)

with open(DATA_DIR / "girl_names_set.pkl", "rb") as f:
    girl_names = pickle.load(f)
    
from utils.name_loader import boy_names, girl_names
