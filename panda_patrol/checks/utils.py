import os
import importlib
import os

skipped = set(["check.py", "constants.py", "utils.py"])


def import_all_modules_from_directory():
    modules = {}
    for filename in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        if (
            filename.endswith(".py")
            and not filename.startswith("__")
            and filename not in skipped
        ):
            module_name = filename[:-3]  # Remove '.py' from the end
            module = importlib.import_module(f"panda_patrol.checks.{module_name}")
            modules[module_name] = module
    return modules
