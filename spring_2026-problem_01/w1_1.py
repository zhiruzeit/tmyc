import pandas as pd
import os

def read_csv(path: str, id_name: str) -> pd.DataFrame:
    # Use these column header names instead
    column_names = [id_name, 'Red Eggs', 'Blue Eggs', 'Yellow Eggs', 'Green Eggs', 'Pink Eggs']

    # Read the CSV (seperate by any number of spaces, no header)
    df = pd.read_csv(path, sep=r'\s+', header=None, names=column_names)
    
    # Drop duplicates before returning
    return df.drop_duplicates(subset=[id_name])


def intersect_dataframes_by_id(dfs: list[pd.DataFrame], id_name: str) -> pd.DataFrame:
    # Set the column name to use to intersect the matching ID
    dfs_indexed = [df.set_index([id_name]) for df in dfs]

    # Intersect along the index (axis=1 for horizontal concat, join='inner' for intersection)
    df_intersection = pd.concat(dfs_indexed, axis=1, join='inner').reset_index()

    return df_intersection

if __name__ == "__main__":
    id_name = 'Employee ID'

    # Get full CSV relative paths from csv folder
    csv_files = [os.path.join('csv', f) for f in os.listdir('csv') if f.endswith('.csv')]

    # Read CSVs
    dfs = [read_csv(path, id_name) for path in csv_files]

    # Intersect DataFrames by Employee ID
    weekly_bunny_ids = intersect_dataframes_by_id(dfs, id_name)
    
    # Total number unique Employee IDs
    num_weekly_bunnies = weekly_bunny_ids[id_name].nunique()

    # Print total number of good bunnies
    print(num_weekly_bunnies)