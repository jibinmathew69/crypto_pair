import pyarrow.feather as feather
import pandas as pd

def read_file(filename):
    try:
        read_df = feather.read_feather(filename)
    except:
        return False

    return read_df

def write_file(df, filename):

    try:
        with open(filename, 'wb') as f:
            feather.write_feather(df, f)
    except:
        return False

    return True
    
def append_file(df, filename):
    try:
        read_df = feather.read_feather(filename)
        df = pd.concat([read_df, df])
        with open(filename, 'wb') as f:
            feather.write_feather(df, f)
    except:
        return False

    return True
    