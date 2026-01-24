"""Job board API routes"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from app.schemas.job import Job, JobFilters, JobRecommendation
from app.services.job_service import JobService

logger = logging.getLogger(__name__)
router = APIRouter()

job_service = JobService()


@router.get("/jobs", response_model=List[Job])
async def get_jobs(
    search: Optional[str] = Query(None, description="Search query"),
    location: Optional[str] = Query(None, description="Location filter"),
    type: Optional[str] = Query(None, description="Job type filter"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    minSalary: Optional[float] = Query(None, description="Minimum salary"),
    maxSalary: Optional[float] = Query(None, description="Maximum salary"),
):
    """Get all jobs with optional filters"""
    try:
        filters = JobFilters(
            search=search,
            location=location,
            type=type,
            tags=tags.split(",") if tags else None,
            minSalary=minSalary,
            maxSalary=maxSalary,
        )
        jobs = await job_service.get_jobs(filters)
        return jobs
    except Exception as e:
        logger.error(f"Error fetching jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch jobs")


@router.get("/jobs/recommendations", response_model=List[JobRecommendation])
async def get_recommendations(
    limit: Optional[int] = Query(10, ge=1, le=50, description="Number of recommendations")
):
    """Get personalized job recommendations"""
    try:
        recommendations = await job_service.get_recommendations(limit)
        return recommendations
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch recommendations")


@router.get("/jobs/{job_id}", response_model=Job)
async def get_job_by_id(job_id: str):
    """Get a specific job by ID"""
    try:
        job = await job_service.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch job")

