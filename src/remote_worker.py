import os
import platform
from typing import Any

import psutil
from arq.connections import RedisSettings
from hyko_sdk.models import StorageConfig
from hyko_toolkit.registry import Registry

REDIS_SETTINGS = RedisSettings(
    host=f"redis.{os.getenv('HOST')}",
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASS"),
)

async def ping_worker(ctx: Any):
    """Check if the worker is online."""
    return "pong"


async def get_system_info(ctx: Any):
    """Arq task to get system info of worker."""
    system_info = {
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "cpu_cors": os.cpu_count(),
        "total_memory": psutil.virtual_memory().total / (1024 ** 3)
    }

    return system_info

async def execute_node(
    ctx: dict[str, Any],
    function_image: str,
    inputs: dict[str, Any],
    params: dict[str, Any],
    refresh_token: str,
    access_token: str,
):
    """Celery task to execute in worker."""
    node = Registry.get_handler(function_image)

    output = await node.call(
        inputs,
        params,
        storage_config=StorageConfig(
            refresh_token=refresh_token,
            access_token=access_token,
            host=f"https://api.{os.getenv('HOST')}",
        ),
    )

    return output.model_dump()


class WorkerSettings:
    """WorkerSettings defines the settings to use when creating the work.

    It's used by the arq CLI.
    redis_settings might be omitted here if using the default settings
    For a list of all available settings, see https://arq-docs.helpmanual.io/#arq.worker.Worker
    """

    functions = [execute_node, get_system_info, ping_worker]
    redis_settings = REDIS_SETTINGS
    queue_name = os.getenv("QUEUE_NAME")
