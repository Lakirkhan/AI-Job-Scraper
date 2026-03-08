"""
Job Skill Filter Module
Filters jobs based on required skills
"""

from utils.config import JOB_SKILLS

class SkillFilter:
    def __init__(self, required_skills=None):
        self.required_skills = required_skills or JOB_SKILLS
    
    def filter_jobs(self, jobs):
        """
        Filter jobs by required skills
        
        Args:
            jobs (list): List of job dictionaries
            
        Returns:
            list: Filtered jobs that match required skills
        """
        filtered_jobs = []
        
        for job in jobs:
            if self._matches_skills(job):
                filtered_jobs.append(job)
        
        matched_count = len(filtered_jobs)
        original_count = len(jobs)
        filtered_count = original_count - matched_count
        
        print(f"ℹ Skill Filter: {matched_count}/{original_count} jobs matched ({filtered_count} filtered out)")
        
        return filtered_jobs
    
    def _matches_skills(self, job):
        """
        Check if job matches required skills
        
        Args:
            job (dict): Job dictionary
            
        Returns:
            bool: True if job matches any required skill
        """
        # Check title
        title = (job.get('title', '') or '').lower()
        
        # Check description if available
        description = (job.get('description', '') or '').lower()
        
        # Combine text to search
        combined_text = f"{title} {description}"
        
        # Check for skill matches (at least one skill should be found)
        for skill in self.required_skills:
            skill_lower = skill.lower()
            
            # Use word boundary matching for better accuracy
            if f" {skill_lower} " in f" {combined_text} ":
                return True
            
            # Also check without word boundaries for compound words
            if skill_lower in combined_text:
                return True
        
        return False
    
    def filter_by_custom_skills(self, jobs, skills):
        """
        Filter jobs by custom skill list
        
        Args:
            jobs (list): List of job dictionaries
            skills (list): Custom list of skills to filter
            
        Returns:
            list: Filtered jobs
        """
        original_filter = self.required_skills
        self.required_skills = skills
        filtered = self.filter_jobs(jobs)
        self.required_skills = original_filter
        return filtered

def filter_jobs(jobs, skills=None):
    """Backward compatible function"""
    skill_filter = SkillFilter(skills or JOB_SKILLS)
    return skill_filter.filter_jobs(jobs)