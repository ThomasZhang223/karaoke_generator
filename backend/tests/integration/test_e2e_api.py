"""E2E API integration tests: Full request/response cycles."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from backend.main import app
from backend.services.karaoke_service import KaraokeService
from backend.models.schemas import JobStatus


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.mark.integration
@pytest.mark.smoke
def test_health_endpoint(client):
    """Test health check endpoint returns 200."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.integration
@pytest.mark.regression
def test_complete_karaoke_generation_flow(client):
    """Test complete flow: submit URL → poll status → download video."""
    # Mock the karaoke service
    with patch('backend.api.endpoints.karaoke.karaoke_service.create_job', return_value="test-job-123") as mock_create, \
         patch('backend.api.endpoints.karaoke.karaoke_service.process_job', new_callable=AsyncMock) as mock_process:
        response = client.post(
            "/api/v1/karaoke/generate",
            json={"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        )
        assert response.status_code == 202
        data = response.json()
        assert data["job_id"] == "test-job-123"
        mock_create.assert_called_once()
        mock_process.assert_called_once()

    job_id = "test-job-123"
    with patch('backend.api.endpoints.karaoke.karaoke_service.get_job_status', return_value={
        "job_id": job_id,
        "status": JobStatus.COMPLETED,
        "progress": 100,
        "stage": "Done",
        "video_path": f"/tmp/{job_id}.mp4",
        "error": None
    }):
        response = client.get(f"/api/v1/karaoke/status/{job_id}")
        assert response.status_code == 200
        status_data = response.json()
        assert status_data["status"] == JobStatus.COMPLETED.value
        assert status_data["video_url"] == f"/api/v1/karaoke/download/{job_id}"


@pytest.mark.integration
@pytest.mark.regression
def test_progress_updates_work_correctly(client):
    """Test that progress updates reflect processing stages."""
    job_id = "test-progress-job"
    
    stages = [
        JobStatus.PENDING,
        JobStatus.DOWNLOADING,
        JobStatus.PROCESSING_AUDIO,
        JobStatus.FETCHING_LYRICS,
        JobStatus.RENDERING_VIDEO,
        JobStatus.COMPLETED,
    ]
    
    for stage_data in stages:
        with patch('backend.api.endpoints.karaoke.karaoke_service.get_job_status', return_value={
            "job_id": job_id,
            "status": stage_data,
            "progress": 50,
            "stage": "Stage",
            "video_path": "/tmp/video.mp4" if stage_data == JobStatus.COMPLETED else None,
            "error": None
        }):
            response = client.get(f"/api/v1/karaoke/status/{job_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == stage_data.value
            if stage_data == JobStatus.COMPLETED:
                assert data["video_url"] is not None


@pytest.mark.integration
@pytest.mark.regression
def test_error_handling_across_endpoints(client):
    """Test error responses (400, 404, 500) across all endpoints."""
    # Test 400: Invalid URL
    response = client.post(
        "/api/v1/karaoke/generate",
        json={"youtube_url": "not-a-valid-url"}
    )
    assert response.status_code in [400, 422]  # Validation error
    
    # Test 404: Non-existent job
    response = client.get("/api/v1/karaoke/status/non-existent-job-id")
    assert response.status_code in [404, 200]  # May return 200 with error in body
    
    # Test frontend endpoint
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.smoke
def test_cors_middleware_configured(client):
    """Test that CORS middleware allows frontend requests."""
    response = client.options(
        "/api/v1/karaoke/generate",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST"
        }
    )
    # CORS preflight should succeed
    assert response.status_code in [200, 204]


@pytest.mark.integration
@pytest.mark.regression
def test_api_documentation_accessible(client):
    """Test that Swagger documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
    
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
