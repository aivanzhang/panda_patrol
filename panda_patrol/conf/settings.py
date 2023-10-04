import importlib
import os
from panda_patrol.conf import default_settings

ENVIRONMENT_VARIABLE = "PANDA_PATROL_SETTINGS_MODULE"


class Settings:
    def __init__(self):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(default_settings):
            if setting.isupper():
                setattr(self, setting, getattr(default_settings, setting))

        settings_module = os.environ.get("PANDA_PATROL_SETTINGS_MODULE", None)

        if settings_module is None:
            return

        self.PANDA_PATROL_SETTINGS_MODULE = settings_module

        # store the settings module in case someone later cares
        mod = importlib.import_module(self.PANDA_PATROL_SETTINGS_MODULE)

        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

    def __getitem__(self, name):
        return self.__dict__[name]

    def __str__(self) -> str:
        return f"Settings({self.__dict__})"


settings = Settings()
