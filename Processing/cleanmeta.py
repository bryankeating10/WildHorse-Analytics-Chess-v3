import pandas as pd

# Remove unecessary columns
def remove_unnec(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove unnecessary columns from the metadata DataFrame.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame

    Returns:
    --------
    pd.DataFrame
        DataFrame with specified columns removed
    """
    df = df.copy()
    cols_to_remove = ['Event','Site','Round','CurrentPosition','Timezone','ECOUrl','UTCTime','Link']
    df.drop(columns=cols_to_remove, inplace=True, errors='ignore')
    return df

# Convert date and time columns to datetime
def convert_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date and time columns to datetime objects.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame with 'UTCDate', 'StartTime', 'EndDate', 'EndTime' columns

    Returns:
    --------
    pd.DataFrame
        DataFrame with new 'StartDateTime' and 'EndDateTime' columns
    """
    df = df.copy()
    df['StartDateTime'] = pd.to_datetime(df['UTCDate'] + ' ' + df['StartTime'])
    df['EndDateTime'] = pd.to_datetime(df['EndDate'] + ' ' + df['EndTime'])
    df.drop(columns=['UTCDate', 'StartTime', 'EndDate', 'EndTime'], inplace=True, errors='ignore')
    return df

# Map results to integers
def map_results(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map game results from strings to integers.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame with 'Result' column

    Returns:
    --------
    pd.DataFrame
        DataFrame with 'Result' column mapped to integers
    """
    df = df.copy()
    result_map = {
        '0-1': 0,
        '1-0': 1,
        '1/2-1/2': 2
    }
    df['Result'] = df['Result'].map(result_map).astype('uint8')
    return df

# Helper function for termination mapping
def term_helper(value:str) -> int:
    val = value.lower()
    termination_map = {
        'won by checkmate': 0,
        'won by resignation': 1,
        'won on time': 2,
        'won - game abandoned': 3,
        'game drawn by stalemate': 4,
        'game drawn by repetition': 5,
        'game drawn by insufficient material': 6,
        'game drawn by 50-move rule': 7,
        'game drawn by timeout vs insufficient material': 8,
        'game drawn by agreement': 9
    }
    for substr, code in termination_map.items():
        if substr in val:
            return code
    return 10   # unexpected termination value


# Use term_helper to map values
def map_termination(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map game termination reasons from strings to integers.

    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame with 'Termination' column

    Returns:
    --------
    pd.DataFrame
        DataFrame with 'Termination' column mapped to integers
    """
    df = df.copy()
    df['Termination'] = df['Termination'].apply(term_helper).astype('uint8')
    return df