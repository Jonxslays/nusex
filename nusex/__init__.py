__productname__ = "nusex"
__version__ = "0.2.0.dev2"
__description__ = "A project templating utility for Python."
__url__ = "https://github.com/parafoxia/nusex"
__docs__ = "https://nusex.readthedocs.io/en/latest/"
__author__ = "Ethan Henderson"
__author_email__ = "ethan.henderson.1998@gmail.com"
__license__ = "BSD 3-Clause"
__bugtracker__ = "https://github.com/parafoxia/nusex/issues"

import os
from pathlib import Path

if os.name == "nt":
    CONFIG_DIR = Path.home() / ".nusex"
else:
    CONFIG_DIR = Path.home() / ".config/nusex"

from . import commands
