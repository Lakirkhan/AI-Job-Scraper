"""
CSV Exporter Module
Exports job listings to CSV format
"""

import csv
from datetime import datetime
from utils.config import OUTPUT_FOLDER, CSV_PREFIX
import os

class CSVExporter:
    def __init__(self):
        self.output_folder = OUTPUT_FOLDER
        self._ensure_output_folder()
    
    def _ensure_output_folder(self):
        """Create output folder if it doesn't exist"""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            print(f"✓ Created output folder: {self.output_folder}")
    
    def export(self, jobs, filename=None):
        """
        Export jobs to CSV
        
        Args:
            jobs (list): List of job dictionaries
            filename (str): Custom filename (optional)
            
        Returns:
            str: Path to saved file
        """
        if not jobs:
            print("⚠ No jobs to export to CSV")
            return None
        
        try:
            # Create filename
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M')
                filename = f"{CSV_PREFIX}{timestamp}.csv"
            
            filepath = os.path.join(self.output_folder, filename)
            
            # Get headers from first job
            headers = list(jobs[0].keys()) if jobs else []
            
            # Write CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(jobs)
            
            print(f"✓ CSV exported: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"✗ Error exporting to CSV: {str(e)}")
            return None

def export_jobs_csv(jobs, filename=None):
    """Backward compatible function"""
    exporter = CSVExporter()
    return exporter.export(jobs, filename)
