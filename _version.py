__version__ = open("version.txt", "r").read()
__author__ = 'Notch'
__email__ = 'imnotch_xvi@gmail.com'

from datetime import datetime

current_date = datetime.now()
formatted_date = f"v.{current_date.day:02d}.{current_date.month:02d}.{current_date.year}"

open("version.txt", "w").write(formatted_date)