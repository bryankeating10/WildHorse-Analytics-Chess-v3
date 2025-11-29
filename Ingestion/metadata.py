import chess.pgn as ch
import pandas as pd
from pathlib import Path

class MetaData:
    """
    Extract game-level metadata from a PGN file and store as DataFrame.
    """
    def __init__(self, pgn_path: str):
        self.project_root = Path(__file__).resolve().parents[1]
        self.pgn_path = self.project_root / Path(pgn_path)
        self.df = self._extract_metadata()
    
    def _extract_metadata(self) -> pd.DataFrame:
        """Read the PGN file and extract metadata for all games."""
        metadata_list = []
        
        with open(self.pgn_path, encoding="utf-8", errors="ignore") as pgn:
            game_id = 1
            while True:
                game = ch.read_game(pgn)
                if game is None:
                    break
                
                headers = dict(game.headers)
                headers["game_id"] = game_id
                game_id += 1
                metadata_list.append(headers)
        
        if not metadata_list:
            return pd.DataFrame()
        
        df = pd.DataFrame(metadata_list)
        df.set_index("game_id", inplace=True)
        return df
    
    def save_csv(self, output_path: str) -> None:
        """Save metadata as CSV to Data/Silver directory."""
        
        self.df.to_csv(output_path, index=True)
        print(f"Saved to {output_path}")