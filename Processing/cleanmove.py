import pandas as pd

# Change white and black to boolean
def convert_color(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert 'color' column from 'white'/'black' to boolean True/False.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with 'color' column

    Returns:
    --------
    pd.DataFrame
        DataFrame with 'color' as boolean
    """
    df = df.copy()
    df['color'] = df['color'].astype(str).eq('white')
    return df