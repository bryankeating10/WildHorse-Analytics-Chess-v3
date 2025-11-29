import chess
import chess.pgn as ch
import pandas as pd
from pathlib import Path


class MoveData:
    """
    Extract move-level data from a PGN file.
    Each row = one ply (half-move).
    """

    def __init__(self, pgn_path: str):
        self.project_root = Path(__file__).resolve().parents[1]
        self.pgn_path = self.project_root / Path(pgn_path)
        self.df = self._extract_moves()

    # ---------------------------------------------------------
    def _extract_moves(self) -> pd.DataFrame:
        moves_list = []
        
        with open(self.pgn_path, encoding="utf-8", errors="ignore") as pgn:

            game_id = 1  # match MetaData integer game_id

            while True:
                game = ch.read_game(pgn)
                if game is None:
                    break

                board = game.board()
                ply = 1

                for node in game.mainline():
                    if node.move is None:
                        continue

                    move = node.move
                    san = board.san(move)

                    # Detect color BEFORE pushing the move
                    color = "white" if board.turn == chess.WHITE else "black"

                    # Extract clock and eval annotations if present
                    clock = None
                    eval = None

                    if node.comment:
                        import re
                        clk_match = re.search(r"\[%clk\s*([0-9:.]+)\]", node.comment)
                        if clk_match:
                            clock = clk_match.group(1)
                        eval_match = re.search(r"\[%eval\s*([#\-\d\.]+)\]", node.comment)
                        if eval_match:
                            eval_str = eval_match.group(1)
                            if eval_str.startswith("#"):
                                eval = f"M{eval_str[1:]}"  # mate in N
                            else:
                                try:
                                    eval = float(eval_str)
                                except ValueError:
                                    eval = None

                    # Apply move first, then get FEN after move
                    board.push(move)
                    fen_after = board.fen()

                    # Store row
                    moves_list.append({
                        "game_id": game_id,
                        "ply": ply,
                        "color": color,
                        "move": san,
                        "clock": clock,
                        "eval": eval,
                        "fen": fen_after,
                    })

                    ply += 1

                game_id += 1
        
        if not moves_list:
            return pd.DataFrame()

        df = pd.DataFrame(moves_list)

        # Sorting ensures stable ordering
        df.sort_values(by=["game_id", "ply"], inplace=True)

        # Reorder columns
        desired_order = ["game_id", "ply", "color", "move", "clock", "eval", "fen"]
        df = df[desired_order]

        return df

    # ---------------------------------------------------------
    def save_csv(self, output_path: str) -> None:
        """Save move data as CSV to Data/Raw directory."""
        
        self.df.to_csv(output_path, index=False)
        print(f"Saved to {output_path}")