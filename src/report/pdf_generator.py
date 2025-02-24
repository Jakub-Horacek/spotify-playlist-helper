from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import matplotlib.pyplot as plt
import io
from typing import List, Any
from collections import Counter
from src.utils.helpers import HelperMethods
from datetime import datetime, timedelta
from reportlab.lib.pdfencrypt import StandardEncryption
from reportlab.pdfbase.pdfdoc import PDFInfo, PDFDate
import os

class PDFGenerator:
    def __init__(self, analyzer, output_file: str):
        self.analyzer = analyzer
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        self.output_file = output_file
        
        # Create document info dictionary
        creation_date = datetime.now().strftime('%Y%m%d%H%M%S')
        self.doc_info = {
            'Title': 'Spotify Mood Playlist Analysis',
            'Author': 'Spotify Playlist Helper',
            'Subject': 'Music Analysis Report',
            'Creator': 'Playlist Helper PDF Generator',
            'Producer': 'ReportLab PDF Library',
            'CreationDate': f'D:{creation_date}',
            'ModDate': f'D:{creation_date}'
        }
        
        # Initialize document
        self.doc = SimpleDocTemplate(
            output_file,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        self.styles = getSampleStyleSheet()
        self.helpers = HelperMethods(analyzer)

    def generate_report(self):
        """Generate the Playlist Helper PDF"""
        elements = []
        
        # Build elements list
        self._build_report_elements(elements)
        
        # Set PDF info during build
        self.doc.build(elements, onFirstPage=self._set_pdf_info)

    def _set_pdf_info(self, canvas, doc):
        """Set PDF info during document build"""
        for key, value in self.doc_info.items():
            canvas.setTitle(self.doc_info['Title'])
            canvas.setAuthor(self.doc_info['Author'])
            canvas.setSubject(self.doc_info['Subject'])
            canvas.setCreator(self.doc_info['Creator'])
            canvas.setProducer(self.doc_info['Producer'])

    def _create_chart(self, data, title, chart_type='pie'):
        """Create charts for the report"""
        plt.figure(figsize=(8, 6))
        
        if chart_type == 'pie':
            plt.pie(
                [v for k, v in data.most_common(5)],
                labels=[k for k, v in data.most_common(5)],
                autopct='%1.1f%%'
            )
        elif chart_type == 'bar':
            items = data.most_common(10)
            plt.bar([k for k, v in items], [v for k, v in items])
            plt.xticks(rotation=45)
            
        plt.title(title)
        
        # Save to bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        return buf

    def _build_report_elements(self, elements):
        """Build all elements for the PDF report"""
        # Add each section in order
        self._add_listening_overview(elements)
        self._add_genre_analysis(elements)
        self._add_artist_deep_dive(elements)
        self._add_mood_recommendations(elements)
        self._add_discovery_suggestions(elements)

    def _add_listening_overview(self, elements):
        """Add detailed listening overview section"""
        elements.append(Paragraph("Your Listening Profile", self.styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        # Calculate recent vs overall statistics
        recent_tracks = self.helpers._get_recent_tracks(days=90)  # Use helpers instance
        total_tracks = self.analyzer.track_processor.tracks
        
        # Add statistics
        stats_text = [
            f"Total Unique Artists: {len(self.analyzer.track_processor.artists)}",
            f"Recent Active Artists: {len(self.helpers._get_recent_artists(days=90))}",  # Use helpers
            f"Average Daily Listening Time: {self.helpers._calculate_daily_average():.1f} hours",  # Use helpers
            f"Most Active Listening Time: {self.helpers._get_peak_listening_hours()}"  # Use helpers
        ]
        
        for stat in stats_text:
            elements.append(Paragraph(stat, self.styles['Normal']))
            elements.append(Spacer(1, 8))
        
        elements.append(Spacer(1, 24))

    def _add_genre_analysis(self, elements):
        """Add detailed genre analysis"""
        elements.append(Paragraph("Genre Preferences", self.styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        # Add genre distribution chart
        elements.append(Paragraph("Your Genre Distribution", self.styles['Heading2']))
        genre_chart = self._create_chart(
            self.helpers._analyze_genres(),
            "Genre Distribution",
            chart_type='pie'
        )
        elements.append(Image(genre_chart, width=400, height=300))
        elements.append(Spacer(1, 24))

    def _add_artist_deep_dive(self, elements):
        """Add detailed analysis with both recent and lifetime stats for artists, songs, and genres"""
        elements.append(Paragraph("Listening Analysis", self.styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        # Calculate date range for recent stats (90 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        date_range = f"(last 90 days - from {start_date.strftime('%d.%m.%Y')} to {end_date.strftime('%d.%m.%Y')})"
        
        # Artists Section
        elements.append(Paragraph("Artist Analysis", self.styles['Heading2']))
        elements.append(Paragraph(f"Your Recent Favorite Artists {date_range}", self.styles['Heading3']))
        recent_artists = self.helpers._get_recent_artists(days=90)
        
        artist_data = [['Artist', 'Play Count', 'Total Time']]
        for artist, count in recent_artists.most_common(15):
            play_time = self.helpers._calculate_artist_playtime(artist)
            artist_data.append([artist, str(count), f"{play_time:.1f} hours"])
        
        table = Table(artist_data, colWidths=[250, 100, 100])
        self._apply_table_style(table)
        elements.append(table)
        elements.append(Spacer(1, 24))
        
        # All-time Artists
        elements.append(Paragraph("Your All-Time Favorite Artists", self.styles['Heading3']))
        all_time_artists = Counter()
        for track in self.analyzer.track_processor.tracks.values():
            all_time_artists[track.artist] += track.play_count
        
        lifetime_data = [['Artist', 'Play Count', 'Total Time']]
        for artist, count in all_time_artists.most_common(15):
            play_time = self.helpers._calculate_artist_playtime(artist)
            lifetime_data.append([artist, str(count), f"{play_time:.1f} hours"])
        
        lifetime_table = Table(lifetime_data, colWidths=[250, 100, 100])
        self._apply_table_style(lifetime_table)
        elements.append(lifetime_table)
        elements.append(Spacer(1, 24))
        
        # Songs Section
        elements.append(Paragraph("Song Analysis", self.styles['Heading2']))
        elements.append(Paragraph(f"Your Recent Favorite Songs {date_range}", self.styles['Heading3']))
        recent_tracks = self.helpers._get_recent_tracks(days=90)
        
        track_data = [['Song', 'Artist', 'Play Count']]
        for track_key, count in recent_tracks.most_common(15):
            track = self.analyzer.track_processor.tracks[track_key]
            track_data.append([track.name, track.artist, str(count)])
        
        track_table = Table(track_data, colWidths=[200, 150, 100])
        self._apply_table_style(track_table)
        elements.append(track_table)
        elements.append(Spacer(1, 24))
        
        # All-time Songs
        elements.append(Paragraph("Your All-Time Favorite Songs", self.styles['Heading3']))
        all_time_tracks = Counter()
        for track_key, track in self.analyzer.track_processor.tracks.items():
            all_time_tracks[track_key] = track.play_count
        
        lifetime_track_data = [['Song', 'Artist', 'Play Count']]
        for track_key, count in all_time_tracks.most_common(15):
            track = self.analyzer.track_processor.tracks[track_key]
            lifetime_track_data.append([track.name, track.artist, str(count)])
        
        lifetime_track_table = Table(lifetime_track_data, colWidths=[200, 150, 100])
        self._apply_table_style(lifetime_track_table)
        elements.append(lifetime_track_table)
        elements.append(Spacer(1, 24))
        
        # Genres Section
        elements.append(Paragraph("Genre Analysis", self.styles['Heading2']))
        elements.append(Paragraph(f"Your Recent Favorite Genres {date_range}", self.styles['Heading3']))
        recent_genres = self.helpers._analyze_genres(days=90)
        
        genre_data = [['Genre', 'Play Count', 'Percentage']]
        total_plays = sum(recent_genres.values())
        for genre, count in recent_genres.most_common(10):
            percentage = (count / total_plays * 100) if total_plays > 0 else 0
            genre_data.append([genre, str(count), f"{percentage:.1f}%"])
        
        genre_table = Table(genre_data, colWidths=[200, 100, 150])
        self._apply_table_style(genre_table)
        elements.append(genre_table)
        elements.append(Spacer(1, 24))
        
        # All-time Genres
        elements.append(Paragraph("Your All-Time Favorite Genres", self.styles['Heading3']))
        all_time_genres = self.helpers._analyze_genres()
        
        lifetime_genre_data = [['Genre', 'Play Count', 'Percentage']]
        total_lifetime_plays = sum(all_time_genres.values())
        for genre, count in all_time_genres.most_common(10):
            percentage = (count / total_lifetime_plays * 100) if total_lifetime_plays > 0 else 0
            lifetime_genre_data.append([genre, str(count), f"{percentage:.1f}%"])
        
        lifetime_genre_table = Table(lifetime_genre_data, colWidths=[200, 100, 150])
        self._apply_table_style(lifetime_genre_table)
        elements.append(lifetime_genre_table)
        elements.append(Spacer(1, 24))

    def _apply_table_style(self, table):
        """Apply consistent styling to tables"""
        table.setStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

    def _add_mood_recommendations(self, elements):
        """Add mood-based recommendations"""
        elements.append(Paragraph("Mood-Based Playlist Suggestions", self.styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        moods = {
            "Relaxing": "Ambient, Downtempo, Acoustic",
            "Energetic": "Rock, Electronic, Pop",
            "Melancholic": "Alternative, Indie, Blues",
            "Happy": "Pop, Dance, Feel-good",
            "Focus": "Instrumental, Classical, Minimal"
        }
        
        for mood, genres in moods.items():
            elements.append(Paragraph(f"{mood} Playlist", self.styles['Heading2']))
            elements.append(Paragraph(f"Related Genres: {genres}", self.styles['Normal']))
            elements.append(Spacer(1, 12))
            
            # Add mood-specific recommendations
            top_artists = self.helpers._get_mood_related_artists(mood)
            elements.append(Paragraph("Suggested Artists:", self.styles['Heading3']))
            elements.append(Paragraph(", ".join(top_artists[:10]), self.styles['Normal']))
            elements.append(Spacer(1, 24))

    def _add_discovery_suggestions(self, elements):
        """Add discovery suggestions based on listening patterns"""
        elements.append(Paragraph("Discovery Suggestions", self.styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        # Add suggestions based on listening patterns
        elements.append(Paragraph(
            "Based on your listening history, you might enjoy exploring these areas:",
            self.styles['Normal']
        ))
        elements.append(Spacer(1, 12))
        
        suggestions = self._generate_discovery_suggestions()
        for category, items in suggestions.items():
            elements.append(Paragraph(category, self.styles['Heading2']))
            elements.append(Paragraph(", ".join(items), self.styles['Normal']))
            elements.append(Spacer(1, 12))

    def _generate_discovery_suggestions(self) -> dict:
        """Generate discovery suggestions based on listening patterns"""
        suggestions = {
            "Similar Artists": [],
            "Recommended Genres": [],
            "Hidden Gems": []
        }
    
        # Get top artists and their related artists
        recent_artists = self.helpers._get_recent_artists(days=90)
        top_artists = [artist for artist, _ in recent_artists.most_common(5)]
    
        # Get similar artists suggestions
        similar_artists = self.helpers._get_similar_artists(top_artists)
        suggestions["Similar Artists"] = similar_artists[:8]  # Limit to top 8 suggestions
    
        # Get genre recommendations based on listening history
        genre_suggestions = self.helpers._get_genre_recommendations()
        # Convert genre suggestions dictionary items to a list
        genre_recs = []
        for genre, artists in genre_suggestions.items():
            genre_recs.append(f"{genre}: {', '.join(artists)}")
        suggestions["Recommended Genres"] = genre_recs[:5]  # Top 5 recommended genres
    
        # Find hidden gems (tracks with high play counts but not recent)
        hidden_gems = self.helpers._find_hidden_gems()
        suggestions["Hidden Gems"] = hidden_gems[:6] if hidden_gems else []  # Top 6 hidden gems
    
        return suggestions
