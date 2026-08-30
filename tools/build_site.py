#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from itinerpic.config import Config
from itinerpic.generators.site_generator import SiteGenerator


def main() -> None:
    config = Config.get()
    generator = SiteGenerator(config=config)
    output_path = generator.generate()
    print(f"Static site generated at {output_path}")


if __name__ == "__main__":
    main()
