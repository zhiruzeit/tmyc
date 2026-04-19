import pandas as pd
import os

def read_csv(path: str, id_name: str) -> pd.DataFrame:
    # Use these column header names instead
    column_names = [id_name, 'Red Eggs', 'Blue Eggs', 'Yellow Eggs', 'Green Eggs', 'Pink Eggs']

    # Read the CSV
    df = pd.read_csv(
        path,
        engine='python',
        sep=r'\t',
        header=0, 
        names=column_names, 
        index_col=False
    )

    # Drop duplicates before returning
    return df.drop_duplicates(subset=[id_name])


def intersect_dataframe_ids(dfs: list[pd.DataFrame], id_name: str) -> pd.DataFrame:
    # Set the column name to use to intersect the matching ID
    common_ids = set(dfs[0][id_name])
    for df in dfs[1:]:
        common_ids &= set(df[id_name])

    # Filter each dataframe to only keep rows with those common IDs
    # Stack them on top of each other (axis=0)
    df_filtered_stacked = pd.concat(
        [df[df[id_name].isin(common_ids)] for df in dfs], 
        axis=0
    )

    return df_filtered_stacked

def sum_rows_per_id(df):
    df_totals = df.groupby(id_name).sum().reset_index()

def sum_columns_to_grand_total(df):
    df['Grand Total'] = df_totals.iloc[:, 1:].sum(axis=1)

def sort_highest_desc():
    df_sorted = df_totals.sort_values(by='Grand Total', ascending=False)

if __name__ == "__main__":
    id_name = 'Employee ID'

    # Get full CSV relative paths from csv folder
    csv_files = [os.path.join('csv', f) for f in os.listdir('csv') if f.endswith('.csv')]

    # Read CSVs
    dfs = [read_csv(path, id_name) for path in csv_files]

    print(dfs[1])

    # Intersect DataFrames rows by Employee ID
    weekly_bunny_ids = intersect_dataframe_ids(dfs, id_name)

    # Each unique ID should appear exactly as many times as the number of files
    is_correct = (weekly_bunny_ids[id_name].value_counts() == len(dfs)).all()
    print(f"Did every bunny show up in all files? {is_correct}")

    # Find the bunny with the highest total of eggs of any color 
    # Total all columns and rows per each unique Employee ID into a new 2D dataframe
    sum_rows_df = sum_row_per_id(weekly_bunny_ids)
    print(sum_rows_df)

    sum_cols_df = sum_columns_to_grand_total(sum_rows_df)
    print(sum_cols_df)

    sorted_by_highest_df = sort_highest_desc()
    print(sorted_by_highest_df)