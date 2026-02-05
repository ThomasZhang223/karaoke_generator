import uuid
from datetime import datetime
from pathlib import Path

import pytest
import schemathesis
from fastapi.testclient import TestClient
from hypothesis import HealthCheck, settings

from backend.api.endpoints import karaoke as karaoke_module
from backend.main import app
from backend.models.schemas import JobStatus

client = TestClient(app)
schema_dict = client.get("/openapi.json").json()
schema_dict["openapi"] = "3.0.3"
schema = schemathesis.from_dict(schema_dict, location="/openapi.json")


@pytest.fixture(scope="session")
def temp_output(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp("schemathesis-output")


@pytest.fixture(autouse=True)
def stub_karaoke_service(monkeypatch, temp_output: Path):
    service = karaoke_module.karaoke_service
    service.jobs.clear()

    def fake_create_job(
        youtube_url: str,
        audio_format: str = "mp3",
        audio_bitrate: int = 192,
    ) -> str:
        job_id = str(uuid.uuid4())
        video_path = temp_output / "videos" / f"{job_id}.mp4"
        video_path.parent.mkdir(parents=True, exist_ok=True)
        video_path.write_bytes(b"dummy video")
        service.jobs[job_id] = {
            "job_id": job_id,
            "youtube_url": youtube_url,
            "video_id": "test_video_id",
            "status": JobStatus.COMPLETED,
            "audio_format": audio_format,
            "audio_bitrate": audio_bitrate,
            "created_at": datetime.now().isoformat(),
            "error": None,
            "video_path": str(video_path),
            "progress": 100,
            "stage": "ready",
        }
        return job_id

    async def fake_process_job(job_id: str):
        return service.jobs[job_id]

    def fake_get_job_status(job_id: str):
        return service.jobs.get(job_id)

    monkeypatch.setattr(service, "create_job", fake_create_job)
    monkeypatch.setattr(service, "process_job", fake_process_job)
    monkeypatch.setattr(service, "get_job_status", fake_get_job_status)
    yield
    service.jobs.clear()


@pytest.fixture
def known_job_id() -> str:
    return karaoke_module.karaoke_service.create_job(
        "https://youtu.be/dQw4w9WgXcQ",
        audio_format="mp3",
        audio_bitrate=192,
    )


@schema.parametrize()
@settings(
    deadline=None,
    max_examples=1,
    suppress_health_check=[HealthCheck.function_scoped_fixture],
)
@pytest.mark.filterwarnings("ignore::hypothesis.errors.NonInteractiveExampleWarning")
def test_api_contract(case, known_job_id):
    if case.path_parameters and "job_id" in case.path_parameters:
        case.path_parameters["job_id"] = known_job_id

    if case.method == "POST" and case.path.endswith("/generate"):
        case.body = {
            "youtube_url": "https://youtu.be/dQw4w9WgXcQ",
            "audio_format": "mp3",
            "audio_bitrate": 192,
        }
    elif case.method == "POST" and case.path.endswith("/generate-karaoke"):
        case.body = {
            "youtubeUrl": "https://youtu.be/dQw4w9WgXcQ",
            "quality": "standard",
        }

    response = case.call_asgi(app=app)

    if case.path.endswith("/download/{job_id}"):
        assert response.status_code == 200
        assert response.content  # ensure file-like content exists
        return

    case.validate_response(response)
