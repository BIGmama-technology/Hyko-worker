
import json
import subprocess
import xml.etree.ElementTree as et


class GPU:
    """Represents GPU Data."""

    def __init__(self, gpu_element):
        """Init GPU Class."""
        self.id = gpu_element.get('id')
        self.mem_clock_clocks_gpu = gpu_element.findtext('clocks/mem_clock')
        self.product_name = gpu_element.findtext('product_name')
        self.mem_clock = gpu_element.findtext('max_clocks/mem_clock')
        self.uuid = gpu_element.findtext('uuid')
        self.gpu_util = gpu_element.findtext('utilization/gpu_util')
        self.gpu_temp_slow_threshold = gpu_element.findtext('temperature/gpu_temp_slow_threshold')
        self.gpu_temp_max_threshold = gpu_element.findtext('temperature/gpu_temp_max_threshold')
        self.gpu_temp = gpu_element.findtext('temperature/gpu_temp')
        self.memory_util = gpu_element.findtext('utilization/memory_util')

class NvidiaSmi:
    """Represents NvidiaSmi Data."""

    def __init__(self, xml_data):
        """Init NvidiaSmi class."""
        root = et.fromstring(xml_data)
        self.attached_gpus = root.findtext('attached_gpus')
        self.gpus = [GPU(gpu) for gpu in root.findall('gpu')]

async def nvidia_smi():
    """Get NvidiaSmi information."""
    try:
        result = subprocess.run(['nvidia-smi', '-x', '-q', '-a'], capture_output=True, text=True, check=True)
    except Exception as e:
        print(f"nvidia-smi command failed with error: {e}")
        return None

    xml_output = result.stdout
    try:
        nvidia_smi_data = NvidiaSmi(xml_output)
    except et.ParseError as e:
        print(f"Failed to parse nvidia-smi XML output: {e}")
        return None

    json_output = json.dumps(nvidia_smi_data, default=lambda o: o.__dict__, indent=4)
    return json_output

