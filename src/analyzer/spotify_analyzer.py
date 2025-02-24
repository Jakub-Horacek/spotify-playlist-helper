import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import concurrent.futures
from typing import Dict, List, Set, Tuple
import time
from dataclasses import dataclass
from collections import Counter
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .track_processor import TrackProcessor
from ..data.data_loader import DataLoader

@dataclass
class Track:
    name: str
    artist: str
    album: str = ""
    uri: str = ""
    ms_played: int = 0
    play_count: int = 0

class SpotifyAnalyzer:
    def __init__(self, data_folder: str, max_items: int = 20):
        self.data_loader = DataLoader(data_folder)
        self.track_processor = TrackProcessor()
        self.max_items = max_items
        self.marquee_segments: Dict[str, List[str]] = {}
        
    def analyze(self) -> None:
        data = self.data_loader.load_all_files()
        
        # Process all data
        self.track_processor.process_extended_history(data['extended_history'])
        self.track_processor.process_recent_history(data['recent_history'])
        self._process_marquee_data(data['marquee'])
        
    def get_top_tracks(self, timeframe: str = 'all') -> List[Tuple[str, int]]:
        cutoff_date = self._get_cutoff_date(timeframe)
        
        tracks = [
            (track, stats.ms_played)
            for track, stats in self.track_processor.tracks.items()
            if not cutoff_date or (stats.last_played and stats.last_played >= cutoff_date)
        ]
        
        return sorted(tracks, key=lambda x: x[1], reverse=True)[:self.max_items]
        
    def _get_cutoff_date(self, timeframe: str) -> datetime:
        now = datetime.now()
        if timeframe == 'month':
            return now - timedelta(days=30)
        elif timeframe == 'year':
            return now - timedelta(days=365)
        elif timeframe == '2years':
            return now - timedelta(days=730)
        return None
        
    def _process_marquee_data(self, marquee_data: List[dict]) -> None:
        for item in marquee_data:
            artist = item.get('artistName', '')
            segment = item.get('segment', '')
            if segment:
                if segment not in self.marquee_segments:
                    self.marquee_segments[segment] = []
                self.marquee_segments[segment].append(artist)

    def process_files(self):
        """Process all JSON files concurrently"""
        print("Starting analysis...")
        files = list(self.data_folder.glob("*.json"))
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for file in files:
                futures.append(
                    executor.submit(self.process_file, file)
                )
            concurrent.futures.wait(futures)

    def process_file(self, file_path: Path):
        """Process individual JSON file based on its type"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if "Streaming_History_Audio" in file_path.name:
                self._process_extended_history(data)
            elif "StreamingHistory_music" in file_path.name:
                self._process_recent_history(data)
            elif "Marquee" in file_path.name:
                self._process_marquee(data)
            elif "Playlist" in file_path.name:
                self._process_playlist(data)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def _process_extended_history(self, data: List[dict]):
        """Process extended listening history"""
        for item in data:
            if item.get('skipped', False):
                continue
                
            track = Track(
                name=item.get('master_metadata_track_name', ''),
                artist=item.get('master_metadata_album_artist_name', ''),
                album=item.get('master_metadata_album_album_name', ''),
                uri=item.get('spotify_track_uri', ''),
                ms_played=item.get('ms_played', 0)
            )
            
            self._update_track_stats(track)

    def _update_track_stats(self, track: Track):
        """Update tracking statistics"""
        key = f"{track.name}:{track.artist}"
        
        if key in self.tracks:
            self.tracks[key].ms_played += track.ms_played
            self.tracks[key].play_count += 1
        else:
            self.tracks[key] = track
            self.tracks[key].play_count = 1
            
        self.artists[track.artist] += track.ms_played 