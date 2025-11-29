# WildHorse Analytics: Chess Performance - Version 2
## Project Overview
Our mission is to transfrom chess improvement from intuition-based experimentation to data-driven, purposeful training by systematically analyzing player game data from chess.com. By uncovvering patterns in opening choices, time management, and tactical errors, we provide actionable insights that help players allocate their training effectively to address areas with the highest potential for rating improvement.

## Introduction
Every game played between public Chess.com accounts generates a wealth of data that is saved to archives pointing to each competitor. Game metadata, move choices, and time management data lay dormant in these archives, rich with untapped improvement potential, but effectively unreadable to the human eye. This project extracts and processes that data, applies machine learning techniques to uncover hidden patterns in player behavior, and generates reports that illustrate concrete improvement opportunities invisible through casual analysis.

## Directory Structure
### `Data/`
Stores all raw, intermediate, and polished data files.
Example contents:
* PGN game files (raw data)
* CSV exports of move and metadata dataframes
* DuckDB databases of cleaned metadata and movedata

### `Utils/`
Contains reusable helper functions and shared utilities.
Example contents:
* `download_user.py` — extracts PGN data from player archives
* `clean_meta.py` — stores class for cleaning metadata
* `add_eval.py` — adds engine evaluation to move dataframe

### `Core/`
Defines the core data models and logic.
Example contents:
* `metadata.py` — handles game-level metadata
* `movedata.py` — manages move parsing and timing

<!-- ### `Analysis/`
Contains Jupyter notebooks and scripts used to process and analyze data.
Example contents:
* `analyze_player.ipynb` — analyzes a specific player’s performance
* `opening_statistics.ipynb` — summarizes outcomes by opening -->

<!-- ### `Visuals/`
Stores all generated plots, charts, and other visual artifacts from the analysis notebooks.
Example contents:
* `elo_trend.png` — ELO trend over time for a player
* `move_time_distribution.png` — histogram of time spent per move -->

<!-- ### `Reports/`
Contains final HTML reports or dashboards summarizing analytical findings and visuals.
Example contents:
* `player_summary.html` — per-player summary dashboards
* `opening_report.html` — aggregated opening analysis report -->

<!-- ### `Tests/`
Houses test scripts to ensure data extraction and analytics run correctly.
Example contents:
* `test_metadata_extraction.py`
* `test_move_parsing.py` -->

## Data Workflow
### 📥 Data Ingestion
Chess.com stores complete game data in PGN (Portable Game Notation) files — a standardized format that captures metadata, move sequences, and their respective time stamps. The metadata appears as key-value pairs at the file header:
```
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2014.01.06"]
[White "Hikaru"]
[Black "Godswill"]
[Result "1-0"]
...
```
and move data is stored as either a semi-strucuted list of moves:
```
1.e4 e5 2.Nf3 f5 3.Nxe5 Qf6 4.d4 d6
5.Nc4 fxe4 6.Nc3 Ne7 7.d5 Qg6 8.h3 h5  1-0
```
or a semi-structured list of key-value pairs including move time, engine evaluation, or both:
```
1. e4 { [%eval 0.17] [%clk 0:00:30] } 1... c5 { [%eval 0.19] [%clk 0:00:30] }
2. Nf3 { [%eval 0.25] [%clk 0:00:29] } 2... Nc6 { [%eval 0.33] [%clk 0:00:30] }
3. Bc4 { [%eval -0.13] [%clk 0:00:28] } 3... e6 { [%eval -0.04] [%clk 0:00:30] } 0-1
```
We retrieve all game archives for a player though the Chess.com public API: ```https://api.chess.com/pub/player/bkchessmaster2/games/archives```. This endpoint returns URLs to monthly PGN archives container the player's complete game history.
### {Markdown GitHub Emoji} PGN Conversion
We then merge the monthly PGN files and convert it into pandas dataframes to be prepared for analysis. The game metadata begins it's journey in a format that resembles this example:
{pandas_df.head() example of metadata (raw dataframe without cleaning)}
and the move data is stored in a long dataframe, ultimately categorized by game, and ordered by ply (every half move)
{pandas_df.head() example of move data (raw dataframe without cleaning)}
### {Markdown GitHub Emoji} Dataframe Cleaning
* MetaData
    * Removing unecessary columns such as Game Link, Site, Event, and others.
    * Mapping Result values to 3 categories for white win, white loss, and draw to improve memory efficiency
    * 
* Simplification of metadata columns. Ex color: white -> True, Black -> False.
### Engine Evaluation
* Explain the idea of Stockfish evaluation and a small one-liner of Stockfish functionality and history
* Briefy touch on why it's important to have move evaluation and {a large jump or dip in position evaluation indicates a critical moment. It is extra important to analyze these positions}
### Database Conversion
* Lay out the conversion from finalized pandas dataframes to DuckDB databases. Touch on speed and memory allocation efficiency

## Analysis Catalogue
### External factors
* Time of day
* White or black
* Time control
### Controllable factors
* Blunder ratios
* Checkmate ratios
* Timeout ratios
* Opening choice vs success

## Future Goals
* Expand the analytics to include opponent-based performance metrics.
* Develop an interactive dashboard for browsing player statistics.
* Incorporate machine learning to predict outcomes or detect playstyle trends.

## Resources
- 365Chess. *Chess ECO Codes*. Retrieved from https://www.365chess.com/eco.php