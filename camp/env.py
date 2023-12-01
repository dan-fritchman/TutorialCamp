"""
# Environment 
Load environment variables from a `dotenv` format file. 
Fails if we can't find one. 
Later stuff will generally fail if it lacks the right variables.
"""

import dotenv
from pathlib import Path

# Go look for the file, in parent folders of *this* file.
envfile = dotenv.find_dotenv()
if not envfile:
    this_dir = Path(__file__).parent
    msg = f"Could not find .env file in {this_dir} or any of its parent directories."
    raise RuntimeError(msg)

print(f"Loading environment from {envfile}")
dotenv.load_dotenv(envfile)

# This module is solely for "side effects", not importing anything.
__all__ = []
