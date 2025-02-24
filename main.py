import argparse
import time
from src.analyzer.spotify_analyzer import SpotifyAnalyzer
from src.report.pdf_generator import PDFGenerator
from datetime import datetime
import os

def generate_unique_filename(base_output):
    # Always ensure base_output starts with 'output/'
    if not base_output.startswith('output/'):
        base_output = os.path.join('output', os.path.basename(base_output))
    
    # Get directory and filename parts
    output_dir = os.path.dirname(base_output)
    base_name = os.path.basename(base_output)
    name, ext = os.path.splitext(base_name)
    
    # Create timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create new filename with timestamp
    new_filename = f"{name}_{timestamp}{ext}"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    return os.path.join(output_dir, new_filename)

def main():
    parser = argparse.ArgumentParser(description='Create mood-based playlist recommendations from Spotify listening history')
    parser.add_argument('data_folder', help='Folder containing your Spotify JSON data export files')
    parser.add_argument('--output', default=os.path.join('output', 'spotify_analysis.pdf'), help='Output PDF file')
    parser.add_argument('--max-items', type=int, default=20, help='Maximum items in each category')
    args = parser.parse_args()

    start_time = time.time()
    print("Starting Spotify listening history analysis...")
    
    # Generate unique filename
    output_file = generate_unique_filename(args.output)
    
    # Initialize and run analyzer
    analyzer = SpotifyAnalyzer(args.data_folder, args.max_items)
    analyzer.analyze()
    
    # Generate PDF report
    print("Generating PDF report...")
    pdf_gen = PDFGenerator(analyzer, output_file)
    pdf_gen.generate_report()
    
    elapsed_time = time.time() - start_time
    print(f"Analysis complete! Time taken: {elapsed_time:.2f} seconds")
    print(f"Report saved to: {output_file}")

if __name__ == "__main__":
    main()
