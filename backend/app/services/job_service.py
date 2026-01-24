"""Job service with mock data"""
from typing import List, Optional
from datetime import datetime, timedelta
import random

from app.schemas.job import Job, JobFilters, JobRecommendation, MatchBreakdown

def format_time_ago(days: int, hours: int = 0) -> str:
    """Format time posted"""
    if hours > 0:
        return f"{hours} hours ago"
    if days == 0:
        return "Today"
    if days == 1:
        return "1 day ago"
    return f"{days} days ago"

# Mock job data matching Figma design
MOCK_JOBS = [
    {
        "id": "1",
        "title": "Web Application Developer",
        "company": "Backd Business Funding",
        "location": "Austin, Texas Metropolitan Area",
        "type": "full-time",
        "workType": "on-site",
        "salary": {"min": 65000, "max": 70000, "currency": "USD"},
        "description": "We're looking for a web application developer to join our team. You'll work on building scalable web applications using modern technologies.",
        "requirements": ["3+ years experience", "JavaScript", "React", "Node.js"],
        "tags": ["Web Development", "JavaScript", "React"],
        "postedDate": (datetime.now() - timedelta(hours=1)).isoformat(),
        "featured": False,
        "logo": None,
        "matchPercentage": 64.0,
        "matchBreakdown": {
            "education": 70.0,
            "skills": 60.0,
            "workExp": 65.0,
            "expLevel": 62.0
        },
        "skillsMatch": "0 of 3 skills match",
        "experienceLevel": "Mid Level",
        "applicantCount": 25,
        "timePosted": "1 hours ago",
        "isMatched": True,
        "isLiked": False,
        "isApplied": False,
        "fitExplanation": "You have relevant experience in web development, though some specific skills may need development."
    },
    {
        "id": "2",
        "title": "Software Engineer, Network Infrastructure",
        "company": "Cursor AI",
        "location": "Sunnyvale, CA",
        "type": "full-time",
        "workType": "on-site",
        "salary": {"min": 161000, "max": 239000, "currency": "USD"},
        "description": "Join our team to build network infrastructure systems. Experience with distributed systems, networking protocols, and cloud infrastructure required.",
        "requirements": ["5+ years experience", "Network Infrastructure", "Distributed Systems", "Cloud"],
        "tags": ["Network", "Infrastructure", "Cloud", "Distributed Systems"],
        "postedDate": (datetime.now() - timedelta(hours=2)).isoformat(),
        "featured": True,
        "logo": None,
        "matchPercentage": 93.0,
        "matchBreakdown": {
            "education": 95.0,
            "skills": 92.0,
            "workExp": 94.0,
            "expLevel": 91.0
        },
        "skillsMatch": "5+ years exp",
        "experienceLevel": "Mid Level",
        "applicantCount": 25,
        "timePosted": "2 hours ago",
        "isMatched": True,
        "isLiked": True,
        "isApplied": False,
        "fitExplanation": "You have substantial experience in network infrastructure and distributed systems, making you an excellent fit for this role."
    },
    {
        "id": "3",
        "title": "Full-Stack Software Engineer (Web Developer)",
        "company": "Simons Foundation",
        "location": "New York, NY",
        "type": "full-time",
        "workType": "on-site",
        "salary": {"min": 125000, "max": 140000, "currency": "USD"},
        "description": "Build full-stack web applications for scientific research platforms. Work with modern web technologies and contribute to open-source projects.",
        "requirements": ["5+ years experience", "Full-Stack", "Web Development", "Python", "JavaScript"],
        "tags": ["Full-Stack", "Web Development", "Python", "JavaScript"],
        "postedDate": (datetime.now() - timedelta(days=1)).isoformat(),
        "featured": True,
        "logo": None,
        "matchPercentage": 82.0,
        "matchBreakdown": {
            "education": 85.0,
            "skills": 80.0,
            "workExp": 83.0,
            "expLevel": 80.0
        },
        "skillsMatch": "5+ years exp",
        "experienceLevel": "Mid Level",
        "applicantCount": 27,
        "timePosted": "1 day ago",
        "isMatched": True,
        "isLiked": True,
        "isApplied": True,
        "fitExplanation": "Your full-stack experience aligns well with the requirements, and your background in web development is highly relevant."
    },
    {
        "id": "4",
        "title": "UX Designer",
        "company": "Company name",
        "location": "Ann Arbor, MI",
        "type": "full-time",
        "workType": "remote",
        "salary": {"min": 90000, "max": 130000, "currency": "USD"},
        "description": "Design user experiences for digital products. Work with cross-functional teams to create intuitive and engaging interfaces.",
        "requirements": ["3+ years experience", "UX Design", "User Research", "Prototyping"],
        "tags": ["UX", "Design", "User Research"],
        "postedDate": (datetime.now() - timedelta(days=3)).isoformat(),
        "featured": False,
        "logo": None,
        "matchPercentage": 93.0,
        "matchBreakdown": {
            "education": 93.0,
            "skills": 80.0,
            "workExp": 44.0,
            "expLevel": 85.0
        },
        "skillsMatch": "5+ years exp",
        "experienceLevel": "Mid Level",
        "applicantCount": 15,
        "timePosted": "3 days ago",
        "isMatched": True,
        "isLiked": False,
        "isApplied": False,
        "fitExplanation": "You have substantial experience as a UI/UX Designer, Interaction Designer, and User Research Specialist. Your role at Sohu aligns with designing interaction elements relevant to user experience design for digital products."
    },
    {
        "id": "5",
        "title": "Senior Full-Stack Engineer",
        "company": "TechCorp",
        "location": "San Francisco, CA",
        "type": "full-time",
        "workType": "remote",
        "salary": {"min": 150000, "max": 200000, "currency": "USD"},
        "description": "We're looking for a senior full-stack engineer to join our AI team. You'll work on cutting-edge products using Next.js, Python, and real-time systems.",
        "requirements": ["5+ years experience", "Next.js", "Python", "FastAPI", "Real-time systems"],
        "tags": ["AI", "Full-Stack", "Next.js", "Python", "Remote"],
        "postedDate": (datetime.now() - timedelta(days=2)).isoformat(),
        "featured": True,
        "logo": None,
        "matchPercentage": 88.0,
        "matchBreakdown": {
            "education": 90.0,
            "skills": 85.0,
            "workExp": 88.0,
            "expLevel": 89.0
        },
        "skillsMatch": "5+ years exp",
        "experienceLevel": "Senior",
        "applicantCount": 42,
        "timePosted": "2 days ago",
        "isMatched": True,
        "isLiked": False,
        "isApplied": False,
        "fitExplanation": "Your extensive full-stack experience and expertise in modern web technologies make you an ideal candidate for this senior role."
    },
    {
        "id": "6",
        "title": "AI Product Engineer",
        "company": "InnovateAI",
        "location": "New York, NY",
        "type": "full-time",
        "workType": "hybrid",
        "salary": {"min": 140000, "max": 180000, "currency": "USD"},
        "description": "Join our team to build AI-powered products that shape the future. Experience with AI/ML, real-time systems, and modern web technologies required.",
        "requirements": ["3+ years experience", "AI/ML", "TypeScript", "React", "Node.js"],
        "tags": ["AI", "Product", "TypeScript", "React", "Hybrid"],
        "postedDate": (datetime.now() - timedelta(days=5)).isoformat(),
        "featured": True,
        "logo": None,
        "matchPercentage": 75.0,
        "matchBreakdown": {
            "education": 78.0,
            "skills": 72.0,
            "workExp": 75.0,
            "expLevel": 75.0
        },
        "skillsMatch": "3+ years exp",
        "experienceLevel": "Mid Level",
        "applicantCount": 38,
        "timePosted": "5 days ago",
        "isMatched": True,
        "isLiked": True,
        "isApplied": False,
        "fitExplanation": "Your experience with AI/ML technologies and modern web development aligns well with this product engineering role."
    },
    {
        "id": "7",
        "title": "Backend Developer - Real-Time Systems",
        "company": "StreamTech",
        "location": "Austin, TX",
        "type": "full-time",
        "workType": "remote",
        "salary": {"min": 120000, "max": 160000, "currency": "USD"},
        "description": "Build scalable real-time systems using FastAPI, WebSockets, and modern async patterns. Experience with LiveKit or similar platforms preferred.",
        "requirements": ["4+ years experience", "Python", "FastAPI", "WebSockets", "Async programming"],
        "tags": ["Backend", "Real-Time", "Python", "FastAPI", "Remote"],
        "postedDate": (datetime.now() - timedelta(days=1)).isoformat(),
        "featured": False,
        "logo": None,
        "matchPercentage": 79.0,
        "matchBreakdown": {
            "education": 82.0,
            "skills": 76.0,
            "workExp": 80.0,
            "expLevel": 78.0
        },
        "skillsMatch": "4+ years exp",
        "experienceLevel": "Mid Level",
        "applicantCount": 22,
        "timePosted": "1 day ago",
        "isMatched": True,
        "isLiked": False,
        "isApplied": False,
        "fitExplanation": "Your backend development experience and knowledge of real-time systems make you a strong candidate for this position."
    },
    {
        "id": "8",
        "title": "Frontend Engineer - Next.js",
        "company": "WebFlow",
        "location": "Seattle, WA",
        "type": "full-time",
        "workType": "hybrid",
        "salary": {"min": 130000, "max": 170000, "currency": "USD"},
        "description": "Create beautiful, responsive UIs with Next.js and Tailwind CSS. Experience with Framer Motion and real-time data visualization preferred.",
        "requirements": ["3+ years experience", "Next.js", "TypeScript", "Tailwind CSS", "React"],
        "tags": ["Frontend", "Next.js", "TypeScript", "UI/UX", "Hybrid"],
        "postedDate": (datetime.now() - timedelta(days=3)).isoformat(),
        "featured": False,
        "logo": None,
        "matchPercentage": 85.0,
        "matchBreakdown": {
            "education": 87.0,
            "skills": 83.0,
            "workExp": 85.0,
            "expLevel": 85.0
        },
        "skillsMatch": "3+ years exp",
        "experienceLevel": "Mid Level",
        "applicantCount": 31,
        "timePosted": "3 days ago",
        "isMatched": True,
        "isLiked": False,
        "isApplied": False,
        "fitExplanation": "Your frontend expertise with Next.js and modern React development aligns perfectly with our requirements."
    },
]


class JobService:
    """Service for job-related operations"""
    
    def __init__(self):
        # Convert match breakdown dicts to MatchBreakdown objects
        for job_data in MOCK_JOBS:
            if "matchBreakdown" in job_data and isinstance(job_data["matchBreakdown"], dict):
                job_data["matchBreakdown"] = MatchBreakdown(**job_data["matchBreakdown"])
        self.jobs = [Job(**job) for job in MOCK_JOBS]
    
    async def get_jobs(self, filters: Optional[JobFilters] = None) -> List[Job]:
        """Get jobs with optional filtering"""
        jobs = self.jobs.copy()
        
        if not filters:
            return jobs
        
        # Apply search filter
        if filters.search:
            search_lower = filters.search.lower()
            jobs = [
                job for job in jobs
                if search_lower in job.title.lower()
                or search_lower in job.company.lower()
                or search_lower in job.description.lower()
            ]
        
        # Apply location filter
        if filters.location:
            location_lower = filters.location.lower()
            jobs = [
                job for job in jobs
                if location_lower in job.location.lower()
            ]
        
        # Apply type filter
        if filters.type:
            jobs = [job for job in jobs if job.type == filters.type]
        
        # Apply tags filter
        if filters.tags:
            jobs = [
                job for job in jobs
                if any(tag.lower() in [t.lower() for t in job.tags] for tag in filters.tags)
            ]
        
        # Apply salary filters
        if filters.minSalary:
            jobs = [
                job for job in jobs
                if job.salary and (job.salary.min is None or job.salary.min >= filters.minSalary)
            ]
        
        if filters.maxSalary:
            jobs = [
                job for job in jobs
                if job.salary and (job.salary.max is None or job.salary.max <= filters.maxSalary)
            ]
        
        return jobs
    
    async def get_job_by_id(self, job_id: str) -> Optional[Job]:
        """Get a job by ID"""
        for job in self.jobs:
            if job.id == job_id:
                return job
        return None
    
    async def get_recommendations(self, limit: int = 10) -> List[JobRecommendation]:
        """Get personalized job recommendations"""
        # Sort by match percentage (highest first)
        sorted_jobs = sorted(
            self.jobs,
            key=lambda x: x.matchPercentage or 0,
            reverse=True
        )[:limit]
        
        # Generate recommendations with match breakdown
        recommendations = []
        for job in sorted_jobs:
            score = (job.matchPercentage or 0) / 100.0
            
            reason = "Top matched" if job.matchPercentage and job.matchPercentage >= 90 else "Good match"
            if job.featured:
                reason = "Featured job"
            
            recommendations.append(
                JobRecommendation(
                    job=job,
                    score=score,
                    reason=reason,
                    matchBreakdown=job.matchBreakdown,
                    fitExplanation=job.fitExplanation
                )
            )
        
        return recommendations[:limit]
