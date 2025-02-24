from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List
from dateutil import parser

@dataclass
class Track:
    name: str
    artist: str
    album: str = ""
    uri: str = ""
    ms_played: int = 0
    play_count: int = 0
    last_played: Optional[datetime] = None
    mood: Optional[str] = None

class TrackProcessor:
    def __init__(self):
        self.tracks: Dict[str, Track] = {}
        self.artists: Dict[str, int] = {}
        self.genres: Dict[str, int] = {}
        
    def process_extended_history(self, data: List[dict]) -> None:
        for item in data:
            if item.get('skipped', False):
                continue
                
            track = Track(
                name=item.get('master_metadata_track_name', ''),
                artist=item.get('master_metadata_album_artist_name', ''),
                album=item.get('master_metadata_album_album_name', ''),
                uri=item.get('spotify_track_uri', ''),
                ms_played=item.get('ms_played', 0),
                last_played=self._parse_datetime(item.get('ts', '')) if item.get('ts') else None
            )
            self._update_track_stats(track)

    def _parse_datetime(self, datetime_str: str) -> datetime:
        """Parse datetime string to naive datetime object"""
        # If the datetime is already timezone-aware, convert to naive
        dt = parser.parse(datetime_str)
        if dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)
        return dt

    def process_recent_history(self, data: List[dict]) -> None:
        for item in data:
            track = Track(
                name=item.get('trackName', ''),
                artist=item.get('artistName', ''),
                ms_played=item.get('msPlayed', 0),
                last_played=self._parse_datetime(item.get('endTime', ''))
            )
            self._update_track_stats(track, weight=2)  # Recent history counts double

    def _update_track_stats(self, track: Track, weight: int = 1) -> None:
        key = f"{track.name}:{track.artist}"
        
        if key in self.tracks:
            self.tracks[key].ms_played += track.ms_played * weight
            self.tracks[key].play_count += weight
            if track.last_played and (not self.tracks[key].last_played or 
                track.last_played > self.tracks[key].last_played):
                self.tracks[key].last_played = track.last_played
        else:
            self.tracks[key] = track
            self.tracks[key].play_count = weight
            
        self.artists[track.artist] = self.artists.get(track.artist, 0) + (track.ms_played * weight)
