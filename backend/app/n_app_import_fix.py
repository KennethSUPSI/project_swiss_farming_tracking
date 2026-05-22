from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
backend_root = str(BACKEND_ROOT)
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

# Add the block above immediately after `from pathlib import Path` in:
# backend/app/n_app.py
#
# This lets `python app\n_app.py` find sibling packages such as `db`
# and `blueprints` when run from the backend folder.
