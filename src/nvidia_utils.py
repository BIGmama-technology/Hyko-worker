import subprocess
import xml.etree.ElementTree as et  # noqa: N813
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class GPU(BaseModel):
    """Nvidia-smi GPU model."""

    id: Optional[str]
    mem_clock_clocks_gpu: Optional[str]
    product_name: Optional[str]
    mem_clock: Optional[str]
    uuid: Optional[str]
    gpu_util: Optional[str]
    gpu_temp_slow_threshold: Optional[str]
    gpu_temp_max_threshold: Optional[str]
    gpu_temp: Optional[str]
    memory_util: Optional[str]

class NvidiaSmi(BaseModel):
    """Represents NvidiaSmi Data."""

    attached_gpus: Optional[str]
    gpus: List[GPU]

async def nvidia_smi() -> Optional[Dict[str, Any]]:
    """Get NvidiaSmi information."""
    try:
        result = subprocess.run(['nvidia-smi', '-x', '-q', '-a'], capture_output=True, text=True, check=True)
    except Exception as e:
        print(f"nvidia-smi command failed with error: {e}")
        return None

    xml_output = result.stdout
    try:
        root = et.fromstring(xml_output)
    except et.ParseError as e:
        print(f"Failed to parse nvidia-smi XML output: {e}")
        return None

    gpus = [
        GPU(
            id=gpu.get('id'),
            mem_clock_clocks_gpu=gpu.findtext('clocks/mem_clock'),
            product_name=gpu.findtext('product_name'),
            mem_clock=gpu.findtext('max_clocks/mem_clock'),
            uuid=gpu.findtext('uuid'),
            gpu_util=gpu.findtext('utilization/gpu_util'),
            gpu_temp_slow_threshold=gpu.findtext('temperature/gpu_temp_slow_threshold'),
            gpu_temp_max_threshold=gpu.findtext('temperature/gpu_temp_max_threshold'),
            gpu_temp=gpu.findtext('temperature/gpu_temp'),
            memory_util=gpu.findtext('utilization/memory_util')
        )
        for gpu in root.findall('gpu')
    ]

    nvidia_smi_data = NvidiaSmi(
        attached_gpus=root.findtext('attached_gpus'),
        gpus=gpus
    )

    return nvidia_smi_data.model_dump()
