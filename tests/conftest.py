import os
import time

import pytest
from dotenv import load_dotenv
from testcontainers.compose import DockerCompose


@pytest.fixture(scope="session", autouse=True)
def runtime():
    with DockerCompose(".", compose_file_name="docker-compose.yaml") as compose:
        time.sleep(2)
        compose.wait_for("http://localhost:8080")
        yield compose

        stdout, stderr = compose.get_logs()
        print("\n->>> SESSION RUNTIME LOGS <<<-\n", stdout.decode("utf-8"))


@pytest.fixture(scope="session")
def loadenv(runtime):
    load_dotenv(dotenv_path="local_run.env")


@pytest.fixture(scope="session")
def endpoint(loadenv):
    yield "http://localhost:8080"


@pytest.fixture(scope="session")
def ground_task(loadenv):
    yield {
        "X-Quindar-Task-Env": "local",
        "X-Quindar-Environment": os.getenv("QUINDAR_ENVIRONMENT"),
        "X-Quindar-Task-Type": "ground",
        "X-Quindar-Client-Id": os.getenv("QUINDAR_CLIENT_ID"),
        "X-Quindar-Client-Secret": os.getenv("QUINDAR_CLIENT_SECRET"),
        "X-Quindar-Audience": os.getenv("QUINDAR_AUDIENCE"),
        "X-Quindar-Scope": os.getenv("QUINDAR_SCOPE"),
        "X-Quindar-Auth-Post-Url": os.getenv("QUINDAR_AUTH_URL"),
        "X-Quindar-Org-Id": os.getenv("ORG_ID"),
    }


@pytest.fixture(scope="session")
def contact_task(loadenv):
    yield {
        "X-Quindar-Task-Env": "local",
        "X-Quindar-Environment": "dev",
        "X-Quindar-Task-Type": "contact",
        "X-Quindar-Client-Id": os.getenv("QUINDAR_CLIENT_ID"),
        "X-Quindar-Client-Secret": os.getenv("QUINDAR_CLIENT_SECRET"),
        "X-Quindar-Audience": os.getenv("QUINDAR_AUDIENCE"),
        "X-Quindar-Scope": os.getenv("QUINDAR_SCOPE"),
        "X-Quindar-Auth-Post-Url": os.getenv("QUINDAR_AUTH_URL"),
        "X-Quindar-Org-Id": os.getenv("ORG_ID"),
        "X-Quindar-Connection-String-Id": os.getenv("CONNECTION_STRING"),
        "X-Quindar-Spacecraft-Id": os.getenv("SPACECRAFT_ID"),
        "X-Quindar-Cosmos-Password": os.getenv("QUINDAR_COSMOS_PASSWORD")
    }
