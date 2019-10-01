from pathlib import Path

PROJECT_ROOT = Path(__file__).absolute().parent.parent.parent
DATABASE_ADRESS = f'sqlite:////{str(PROJECT_ROOT.joinpath("db.db"))}'
