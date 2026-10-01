import sqlite3 as sq

import pandas as pd

from src.paths import CENSUS_DB


def read_census_table(table_name):
	"""Read a table from the Census Bureau SQLite database.

	Parameters
	----------
	table_name : str
		Name of the table to read.

	Returns
	-------
	pandas.DataFrame
		Census table as a DataFrame.
	"""
	query = f"SELECT * FROM [{table_name}]"

	with sq.connect(CENSUS_DB) as conn:
		df = pd.read_sql(query, conn)

	return df


#function to categorize rankings per data point
def categorize(value, mean, std):
    if value < mean - std: #if the value is less than the mean minus one standard deviation return below average
        if value < mean - 2 * std: #if the value is less than the mean minus two standard deviations return well below average
            return 0  # well below average
        return 1  # below average
    elif value > mean + std: #if the value is greater than the mean plus one standard deviation return above average
        if value > mean + 2 * std: #if the value is greater than the mean plus two standard deviations return well above average
            return 4  # well above average
        return 3  # above average
    return 2  # average