import json
from pathlib import Path
from typing import Dict, List, Any
from tqdm import tqdm

class DataLoader:
    def __init__(self, data_folder: str):
        self.data_folder = Path(data_folder)
        
    def load_all_files(self) -> Dict[str, List[Any]]:
        data = {
            'extended_history': [],
            'recent_history': [],
            'marquee': [],
            'playlists': []
        }
        
        files = list(self.data_folder.glob("*.json"))
        for file in tqdm(files, desc="Loading files"):
            with open(file, 'r', encoding='utf-8') as f:
                content = json.load(f)
                
                if "Streaming_History_Audio" in file.name:
                    data['extended_history'].extend(content)
                elif "StreamingHistory_music" in file.name:
                    data['recent_history'].extend(content)
                elif "Marquee" in file.name:
                    data['marquee'].extend(content)
                elif "Playlist" in file.name:
                    if isinstance(content, dict) and 'playlists' in content:
                        data['playlists'].extend(content['playlists'])
                    else:
                        data['playlists'].append(content)
                        
        return data
