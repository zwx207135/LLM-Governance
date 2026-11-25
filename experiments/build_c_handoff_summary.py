"""Build the current C-only overview from existing artifacts."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.organize_c_summary import main

if __name__ == "__main__":
    main()
