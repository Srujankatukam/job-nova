"""Pydantic schemas for Job entities"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SalaryRange(BaseModel):
    """Salary range schema"""
    min: Optional[float] = None
    max: Optional[float] = None
    currency: str = "USD"


class MatchBreakdown(BaseModel):
    """Match breakdown schema"""
    education: float = Field(..., ge=0, le=100)
    skills: float = Field(..., ge=0, le=100)
    workExp: float = Field(..., ge=0, le=100)
    expLevel: float = Field(..., ge=0, le=100)


class JobBase(BaseModel):
    """Base job schema"""
    title: str
    company: str
    location: str
    type: str = Field(..., pattern="^(full-time|part-time|contract|internship)$")
    workType: str = Field(default="on-site", pattern="^(on-site|remote|hybrid)$")
    salary: Optional[SalaryRange] = None
    description: str
    requirements: List[str] = []
    tags: List[str] = []
    featured: bool = False
    logo: Optional[str] = None
    # Match data
    matchPercentage: Optional[float] = Field(None, ge=0, le=100)
    matchBreakdown: Optional[MatchBreakdown] = None
    skillsMatch: Optional[str] = None
    experienceLevel: Optional[str] = None
    applicantCount: Optional[int] = None
    timePosted: Optional[str] = None
    # Status indicators
    isMatched: bool = False
    isLiked: bool = False
    isApplied: bool = False
    # Fit explanation
    fitExplanation: Optional[str] = None


class JobCreate(JobBase):
    """Schema for creating a job"""
    pass


class Job(JobBase):
    """Complete job schema with ID and timestamps"""
    id: str
    postedDate: str
    
    class Config:
        from_attributes = True


class JobFilters(BaseModel):
    """Schema for job filtering"""
    search: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None
    tags: Optional[List[str]] = None
    minSalary: Optional[float] = None
    maxSalary: Optional[float] = None


class JobRecommendation(BaseModel):
    """Schema for job recommendation"""
    job: Job
    score: float = Field(..., ge=0, le=1)
    reason: str
    matchBreakdown: Optional[MatchBreakdown] = None
    fitExplanation: Optional[str] = None

