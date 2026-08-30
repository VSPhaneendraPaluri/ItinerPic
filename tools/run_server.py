#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app


def main() -> None:
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=app.config.get("DEBUG", False))


if __name__ == "__main__":
    main()
