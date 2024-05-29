import importlib
import importlib.resources as rc
import os

import hyko_toolkit


def init_all(package_name: str):
    for package in rc.contents(package_name):
        package_path = os.path.join(hyko_toolkit.__path__[0], package)  # type: ignore
        if os.path.isdir(package_path):
            for root, _, files in os.walk(package_path):
                for file in files:
                    if file == "main.py" and ".hykoignore" not in files:
                        module_name = os.path.relpath(
                            os.path.join(root, file), str(rc.files(package_name))
                        )
                        module_name = module_name.replace(os.path.sep, ".")[:-3]

                        _ = importlib.import_module(f"{package_name}.{module_name}")


init_all("hyko_toolkit")
