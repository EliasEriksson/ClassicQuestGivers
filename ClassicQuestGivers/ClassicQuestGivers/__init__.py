from pathlib import Path

"""
Path variables for the project root and database
"""

PROJECT_ROOT = Path(__file__).absolute().parent.parent.parent
DATABASE_ADRESS = f'sqlite:////{str(PROJECT_ROOT.joinpath("db.db"))}'
