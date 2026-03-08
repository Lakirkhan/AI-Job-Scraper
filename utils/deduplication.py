"""
Deduplication Module
Removes duplicate job listings
"""

from utils.config import DUPLICATE_CHECK_FIELDS

class JobDeduploication:
    @staticmethod
    def remove_duplicates(jobs):
        """
        Remove duplicate jobs
        
        Args:
            jobs (list): List of job dictionaries
            
        Returns:
            list: Jobs with duplicates removed
        """
        seen = set()
        unique_jobs = []
        duplicates_count = 0
        
        for job in jobs:
            # Create a tuple of values from fields to check
            key_values = tuple(
                str(job.get(field, '')).lower().strip() 
                for field in DUPLICATE_CHECK_FIELDS
            )
            
            if key_values not in seen:
                seen.add(key_values)
                unique_jobs.append(job)
            else:
                duplicates_count += 1
        
        if duplicates_count > 0:
            print(f"ℹ Removed {duplicates_count} duplicate jobs")
        
        return unique_jobs
    
    @staticmethod
    def verify_no_duplicates(jobs):
        """Verify no duplicate jobs exist"""
        original_count = len(jobs)
        unique_jobs = JobDeduploication.remove_duplicates(jobs)
        
        if len(unique_jobs) < original_count:
            duplicates = original_count - len(unique_jobs)
            print(f"⚠ Found {duplicates} duplicate jobs out of {original_count}")
        
        return unique_jobs

def remove_duplicates(jobs):
    """Backward compatible function"""
    return JobDeduploication.remove_duplicates(jobs)
