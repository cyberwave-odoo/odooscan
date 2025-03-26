from pathlib import Path

# Define project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"