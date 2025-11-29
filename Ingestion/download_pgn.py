"""
Download PGN games from Chess.com user archives to Data/PGN/ directory
Usage:
    from download_pgn import download_pgn
    download_pgn('bkchessmaster2')
    download_pgn('bkchessmaster2', start_date='2024-01', end_date='2024-12')
"""

import requests
from pathlib import Path

def download_pgn(username: str, start_date: str = None, end_date: str = None) -> None:
    username = username.lower()
    
    # Set output directory
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "Data" / "Bronze"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get archive URLs
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    headers = {"User-Agent": "Mozilla/5.0 (Chess PGN Downloader)"}
    
    response = requests.get(url, headers=headers)
    archives = response.json()['archives']
    
    # Filter by date range if specified
    if start_date is not None or end_date is not None:
        filtered_archives = []
        for archive_url in archives:
            year, month = archive_url.split('/')[-2:]
            archive_period = f"{year}-{month}"
            
            # Check if within range (inclusive)
            if start_date is not None and archive_period < start_date:
                continue
            if end_date is not None and archive_period > end_date:
                continue
            
            filtered_archives.append(archive_url)
        
        archives = filtered_archives
    
    # Reverse to get most recent first
    archives = list(reversed(archives))

    all_pgn = []
    
    # Download each month
    for i, archive_url in enumerate(archives, 1):
        month = archive_url.split('/')[-2:]
        print(f"[{i}/{len(archives)}] Downloading {month[0]}/{month[1]}...")
        
        pgn_url = archive_url + "/pgn"
        response = requests.get(pgn_url, headers=headers)
        
        if response.text.strip():
            all_pgn.append(response.text)
    
    # Save to file
    username = username.lower()
    if len(username) > 8:
        username = username[:8]
    output_file = output_dir / f"{username}.pgn"
    content = "\n\n".join(all_pgn).rstrip() + "\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        download_pgn(sys.argv[1])
    else:
        print("Usage: python download_pgn.py <username>")