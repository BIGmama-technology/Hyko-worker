import os
import platform
from typing import Any

import httpx
import psutil
from arq.connections import RedisSettings
from hyko_sdk.models import StorageConfig
from hyko_toolkit.registry import Registry

from src.config import settings
from src.nvidia_utils import nvidia_smi

REDIS_SETTINGS = RedisSettings(
    host=f"redis.{settings.HOST}",
    username=settings.REDIS_USERNAME,
    password=settings.REDIS_PASS,
)


async def ping_worker(ctx: Any):
    """Check if the worker is online."""
    return True


async def get_system_info(ctx: Any):
    """Arq task to get system and nvidia smi info of worker."""
    system_info = {
        "operating_system": platform.system(),
        "os_version": platform.release(),
        "architecture": platform.machine(),
        "cpu_cors": os.cpu_count(),
        "total_memory": round(psutil.virtual_memory().total / (1024**3), 2),
    }
    smi_info = await nvidia_smi()

    payload = {"system_info": system_info, "nvidia_smi": smi_info, "online": True}

    return payload


async def write_system_info(ctx: Any):
    """Write worker's system info on startup."""
    async with httpx.AsyncClient(verify=False) as client:
        system_info = await get_system_info(ctx=ctx)
        response = await client.post(
            settings.URL,
            json=system_info,
        )
        response.raise_for_status()


async def update_worker_status(ctx: Any):
    """Update worker status to offline on shutdown."""
    async with httpx.AsyncClient(verify=False) as client:
        payload = {"online": False}
        response = await client.post(
            settings.URL,
            json=payload,
        )
        response.raise_for_status()


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
            host=f"https://api.{settings.HOST}",
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
    on_startup = write_system_info
    on_shutdown = update_worker_status
    queue_name = settings.WORKER_ID
