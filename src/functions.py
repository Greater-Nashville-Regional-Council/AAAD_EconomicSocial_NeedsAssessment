import sqlite3 as sq

import pandas as pd

from src.paths import CENSUS_DB


def read_census_table(table_name, geographies=None, columns=None):
    """Read and merge horizontally split Census tables from SQLite.

    Parameters
    ----------
    table_name : str
        Base table name, e.g. ACS5_2024_ZCTA.
    geographies : list, optional
        List of GEO_ID values to retrieve.
    columns : list, optional
        List of columns to return. If None, returns all columns.

    Returns
    -------
    pandas.DataFrame
        Combined Census data.
    """

    with sq.connect(CENSUS_DB) as conn:

        #find table or numbered split tables
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type = 'table'",
            conn
        )["name"].tolist()

        if table_name in tables:
            matching_tables = [table_name]
        else:
            matching_tables = sorted(
                [
                    t for t in tables
                    if t.startswith(f"{table_name}_")
                    and t.rsplit("_", 1)[-1].isdigit()
                ],
                key=lambda t: int(t.rsplit("_", 1)[-1])
            )

        if not matching_tables:
            raise ValueError(f"No tables found for {table_name}")

        #get cols for each table
        table_cols = {}

        for table in matching_tables:
            table_cols[table] = [
                row[1]
                for row in conn.execute(
                    f'PRAGMA table_info("{table}")'
                )
            ]

        #ID columns shared across all split tables - should all be FIPS vars or names
        shared_cols = set.intersection(
            *(set(cols) for cols in table_cols.values())
        )

        #keep original column order
        merge_cols = [
            col for col in table_cols[matching_tables[0]]
            if col in shared_cols
        ]

        if not merge_cols:
            raise ValueError("No shared columns found for merging")

        #read columns from each table
        dfs = []

        for table in matching_tables:

            available = table_cols[table]

            if columns is None:
                selected = available
            else:
                selected = [
                    col for col in available
                    if col in columns or col in merge_cols
                ]

                #Skip tables containing no requested columns
                if not any(col not in merge_cols for col in selected):
                    continue

            select_sql = ", ".join(
                f'"{col}"' for col in selected
            )

            query = f'SELECT {select_sql} FROM "{table}"'
            params = []

            if geographies is not None:
                if "GEO_ID" not in available:
                    raise ValueError(f"GEO_ID not found in {table}")

                if not geographies:
                    return pd.DataFrame(columns=columns)

                placeholders = ", ".join(
                    "?" for _ in geographies
                )

                query += f' WHERE "GEO_ID" IN ({placeholders})'
                params = geographies

            df = pd.read_sql_query(
                query, conn, params=params
            )

            #make sure merge keys are unique - should all be FIPS variations
            if df.duplicated(subset=merge_cols).any():
                raise ValueError(
                    f"Duplicate geography identifiers in {table}"
                )

            dfs.append(df)

    if not dfs:
        return pd.DataFrame(columns=columns)

    #merge split tables
    result = dfs[0]

    for df in dfs[1:]:
        result = result.merge(
            df,
            on=merge_cols,
            how="outer",
            validate="one_to_one"
        )

    #return requested columns
    if columns is not None:
        final_cols = [
            col for col in columns
            if col in result.columns
        ]

        result = result[final_cols]

    return result.reset_index(drop=True)


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