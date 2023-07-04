import pint
from functools import lru_cache
from pathlib import Path
import pandas as pd


@lru_cache(maxsize=1)
def read_csv_file(input_file: Path) -> pd.DataFrame:
    """
    Read csv assuming prescribed columns
    """
    data = pd.read_csv(input_file, header=0)
    data = data.fillna('')
    return data


def miles_to_kilometers(miles: float) -> float:
    """
    Convert miles to kilometers
    """
    ureg = pint.UnitRegistry()
    miles = ureg.Quantity(miles, 'mile')
    kilometers = miles.to('kilometer')
    return kilometers.magnitude


