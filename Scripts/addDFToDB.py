from app import engine
import pandas as pd

## Adds a Pandas DataFrame to the given table of the Database
## Returns The DF read from the SQL table as a check.
def add_df(df, tablename, index = False):
    df.to_sql(tablename, con = engine, index = index, if_exists = 'replace')
    return pd.read_sql(tablename, con = engine)

def get_df_from_db(tablename):
    return pd.read_sql(tablename, con = engine)



