import os
from typing import Any

from arq.connections import RedisSettings
from hyko_sdk.definitions import ToolkitAPI, ToolkitUtils
from hyko_sdk.models import StorageConfig
from hyko_toolkit.registry import Registry

REDIS_SETTINGS = RedisSettings(
    host=f"redis.{os.getenv('HOST')}",
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASS"),
)


async def execute_util_function(
    ctx: dict[str, Any],
    function_image: str,
    inputs: dict[str, Any],
    params: dict[str, Any],
    refresh_token: str,
    access_token: str,
):
    """Celery task to execute in worker."""
    function = Registry.get_handler(function_image)
    assert isinstance(function, ToolkitUtils)

    output = await function.execute(
        inputs,
        params,
        storage_config=StorageConfig(
            refresh_token=refresh_token,
            access_token=access_token,
            host=f"https://api.{os.getenv('HOST')}",
        ),
    )

    return output.model_dump()


async def execute_api_function(
    ctx: dict[str, Any],
    function_image: str,
    inputs: dict[str, Any],
    params: dict[str, Any],
    refresh_token: str,
    access_token: str,
):
    """Celery task to execute in worker."""
    function = Registry.get_handler(function_image)
    assert isinstance(function, ToolkitAPI)

    output = await function.execute(
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

    functions = [execute_api_function, execute_util_function]
    redis_settings = REDIS_SETTINGS
    queue_name = os.getenv("QUEUE_NAME")
