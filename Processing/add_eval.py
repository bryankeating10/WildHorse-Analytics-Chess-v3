"""
Stockfish evaluation using the stockfish Python package.

Usage:
    from Utils.add_eval import add_eval
    df_with_evals = add_eval(move_df, depth=15)
"""

import pandas as pd
from stockfish import Stockfish
import chess

# Stockfish path
STOCK_PATH = r"C:\Tools\stockfish\stockfish-windows-x86-64-avx2.exe"


def is_valid_fen(fen: str) -> bool:
    """Check if FEN is valid and represents a legal position."""
    try:
        board = chess.Board(fen)
        return board.is_valid()  # Check if position is actually legal
    except:
        return False

def add_eval(move_df: pd.DataFrame, depth: int = 15) -> pd.DataFrame:
    """
    Add Stockfish evaluation to moves DataFrame.

    Parameters:
    -----------
    move_df : pd.DataFrame
        DataFrame with 'fen' column
    depth : int
        Analysis depth (default: 15)

    Returns:
    --------
    pd.DataFrame
        DataFrame with added 'eval' column
    """
    df = move_df.copy()
    
    # Initialize Stockfish
    stockfish = Stockfish(path=STOCK_PATH, depth=depth)
    
    evals = []
    total = len(df)
    invalid_count = 0
    
    for index, row in df.iterrows():
        fen = row['fen']
        
        # Validate FEN first
        if not is_valid_fen(fen):
            print(f"Invalid FEN at position {index}: {fen[:50]}...")
            evals.append(None)  # Or 0.0
            invalid_count += 1
            continue
        
        try:
            stockfish.set_fen_position(fen)
            evaluation = stockfish.get_evaluation()
            
            # Extract value
            if evaluation['type'] == 'cp':
                eval_value = evaluation['value'] / 100.0  # Convert centipawns
            else:  # mate
                eval_value = f"M{evaluation['value']}"
            
            evals.append(eval_value)
            
        except Exception as e:
            print(f"Error at position {index}: {e}")
            evals.append(None)
        
        # Progress
        if (index + 1) % 50 == 0:
            print(f"Evaluated {index + 1}/{total} positions... ({invalid_count} invalid)")
    
    df['eval'] = evals
    print(f"\n Completed: {total} positions")
    print(f"Invalid FENs: {invalid_count}")
    
    return df