import os
import sys
from pathlib import Path

PYTHON_311 = "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11"
if sys.version_info[:2] != (3, 11) and os.path.exists(PYTHON_311):
    os.execv(PYTHON_311, [PYTHON_311, *sys.argv])

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "UiStuff"))
from app import run

run()
