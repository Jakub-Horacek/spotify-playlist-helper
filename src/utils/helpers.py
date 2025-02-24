from datetime import datetime, timedelta
from collections import Counter

class HelperMethods:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def _get_recent_tracks(self, days=90):
        """Get tracks played in the last X days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_tracks = Counter()
        
        for track_key, track in self.analyzer.track_processor.tracks.items():
            if track.last_played and track.last_played >= cutoff_date:
                recent_tracks[track_key] = track.play_count
            
        return recent_tracks

    def _get_recent_artists(self, days=90):
        """Get artists played in the last X days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_artists = Counter()
        
        for track in self.analyzer.track_processor.tracks.values():
            if track.last_played and track.last_played >= cutoff_date:
                recent_artists[track.artist] += track.play_count
            
        return recent_artists

    def _calculate_daily_average(self):
        """Calculate average daily listening time in hours"""
        total_ms = sum(track.ms_played for track in self.analyzer.track_processor.tracks.values())
        total_hours = total_ms / (1000 * 60 * 60)  # Convert ms to hours
        
        # Get date range from first to last play
        dates = [track.last_played for track in self.analyzer.track_processor.tracks.values() 
                if track.last_played]
        if not dates:
            return 0
        
        date_range = (max(dates) - min(dates)).days + 1
        return total_hours / date_range if date_range > 0 else 0

    def _get_peak_listening_hours(self):
        """Determine peak listening hours"""
        hour_counts = Counter()
        
        for track in self.analyzer.track_processor.tracks.values():
            if track.last_played:
                hour_counts[track.last_played.hour] += track.ms_played
            
        peak_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:2]
        return f"{peak_hours[0][0]:02d}:00-{peak_hours[0][0]+1:02d}:00 and {peak_hours[1][0]:02d}:00-{peak_hours[1][0]+1:02d}:00"

    def _analyze_genres(self, days=None):
        """Analyze genre distribution based on artist genres"""
        # This is a simplified version - in real implementation, you'd want to use
        # Spotify's API to get actual genre information
        genres = Counter({
            "Rock": 0,
            "Electronic": 0,
            "Pop": 0,
            "Hip Hop": 0,
            "Alternative": 0
        })
        
        # Manually classify some artists based on the data we have
        genre_mapping = {
            "Muse": "Rock",
            "Depeche Mode": "Electronic",
            "Twenty One Pilots": "Alternative",
            "Princess Goes": "Alternative",
            "Vulfpeck": "Pop",
            "Nine Inch Nails": "Electronic",
            "Metallica": "Rock"
        }
        
        cutoff_date = datetime.now() - timedelta(days=days) if days else None
        
        for track in self.analyzer.track_processor.tracks.values():
            if track.artist in genre_mapping:
                # Only count if within the date range (if specified)
                if not cutoff_date or (track.last_played and track.last_played >= cutoff_date):
                    genres[genre_mapping[track.artist]] += track.ms_played
        
        return genres

    def _calculate_artist_playtime(self, artist):
        """Calculate total playtime for an artist in hours"""
        total_ms = sum(track.ms_played for track in self.analyzer.track_processor.tracks.values()
                      if track.artist == artist)
        return total_ms / (1000 * 60 * 60)  # Convert ms to hours

    def _get_mood_related_artists(self, mood):
        """Get artists related to specific mood based on listening patterns"""
        # Create mood categories based on audio features and listening patterns
        recent_artists = self._get_recent_artists(days=90)
        top_artists = [artist for artist, _ in recent_artists.most_common(20)]
        
        # Analyze patterns and categorize artists
        mood_artists = {
            "Relaxing": [],
            "Energetic": [],
            "Melancholic": [],
            "Happy": [],
            "Focus": []
        }
        
        # Categorize artists based on their typical genres and your listening patterns
        for artist in top_artists:
            # Add logic here to categorize artists based on their characteristics
            # This is a placeholder - you'd want to implement proper categorization
            pass
        
        return mood_artists.get(mood, [])

    def _generate_discovery_suggestions(self):
        """Generate discovery suggestions based on listening patterns"""
        suggestions = {
            "Similar to Muse": [
                "Radiohead",
                "Nothing But Thieves",
                "Royal Blood",
                "Arctic Monkeys"
            ],
            "Similar to Depeche Mode": [
                "New Order",
                "The Cure",
                "Gary Numan",
                "VNV Nation"
            ],
            "Similar to Princess Goes": [
                "Against Me!",
                "The Dresden Dolls",
                "Amanda Palmer",
                "Laura Jane Grace"
            ]
        }
        return suggestions

    def _get_similar_artists(self, artists: list) -> list:
        """Get similar artists based on input artists list"""
        similar_artists = []
        
        # Use the existing mapping from _generate_discovery_suggestions
        artist_similarities = {
            "Muse": [
                "Radiohead",
                "Nothing But Thieves",
                "Royal Blood",
                "Arctic Monkeys"
            ],
            "Depeche Mode": [
                "New Order",
                "The Cure",
                "Gary Numan",
                "VNV Nation"
            ],
            "Princess Goes": [
                "Against Me!",
                "The Dresden Dolls",
                "Amanda Palmer",
                "Laura Jane Grace"
            ],
            # Add more mappings for other common artists
            "Nine Inch Nails": [
                "Ministry",
                "KMFDM",
                "Front Line Assembly",
                "Skinny Puppy"
            ],
            "Vulfpeck": [
                "Snarky Puppy",
                "Fearless Flyers",
                "Cory Wong",
                "Lawrence"
            ]
        }
        
        # Collect similar artists for each input artist
        for artist in artists:
            if artist in artist_similarities:
                similar_artists.extend(artist_similarities[artist])
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(similar_artists))

    def _get_genre_recommendations(self):
        """Get genre-based recommendations"""
        genre_recommendations = {
            "Rock": [
                "Tool",
                "A Perfect Circle",
                "Queens of the Stone Age",
                "System of a Down"
            ],
            "Electronic": [
                "Front 242",
                "Covenant",
                "VNV Nation",
                "Assemblage 23"
            ],
            "Alternative": [
                "The Dresden Dolls",
                "Placebo",
                "The Decemberists",
                "Modest Mouse"
            ],
            "Pop": [
                "Theo Katzman",
                "Joey Dosik",
                "Lawrence",
                "Lake Street Dive"
            ],
            "Hip Hop": [
                "Run the Jewels",
                "Aesop Rock",
                "MF DOOM",
                "Del the Funky Homosapien"
            ]
        }
        
        # Get the user's top genres based on listening history
        top_genres = self._analyze_genres().most_common(3)
        recommendations = {}
        
        for genre, _ in top_genres:
            if genre in genre_recommendations:
                recommendations[f"Based on your {genre} listening"] = genre_recommendations[genre]
            
        return recommendations

    def _find_hidden_gems(self):
        """Find tracks with high play counts but not played recently"""
        cutoff_date = datetime.now() - timedelta(days=90)  # Not played in last 90 days
        hidden_gems = []
        
        # Get all tracks sorted by play count
        sorted_tracks = sorted(
            self.analyzer.track_processor.tracks.values(),
            key=lambda x: x.play_count,
            reverse=True
        )
        
        # Find tracks with high play counts but not played recently
        for track in sorted_tracks:
            if track.last_played and track.last_played < cutoff_date and track.play_count > 5:
                hidden_gems.append(f"{track.name} by {track.artist}")
                if len(hidden_gems) >= 10:  # Limit to 10 hidden gems
                    break
                
        return hidden_gems
