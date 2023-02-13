import re
import toml

from Config import Config

_CONFIG_FILE_NAME = 'CreateRegularSnapshotsGitConfig.toml'

class ConfigService:
    def __init__(self):
        self._Config = None
        self._RawConfig = None


    def GetConfig(self):
        if self._Config is None:
            self.RefreshConfig()

        return self._Config

    def RefreshConfig(self):
        self._Config = Config()
        self._RawConfig = {}

        self._ReadConfig(_CONFIG_FILE_NAME)
        self._ValidateConfig()
        self._ParseConfig()

    def _ReadConfig(self, filename):
        try:
            self._RawConfig = toml.load(filename)
        except FileNotFoundError as ex:
            raise RuntimeError(f'Config file "{filename}" not found') from ex

    def _ParseConfig(self):
        self._ParseInterval()

        keys = [
            'Patterns'
        ]

        for k in keys:
            if k in self._RawConfig:
                setattr(self._Config, k, self._RawConfig[k])

    def _ValidateConfig(self):
        self._ValidateInterval()


    def _ValidateInterval(self):
        interval = self._RawConfig['Interval']
        regex = r'([0-9.]+s)?([0-9.]+m)?([0-9.]+h)?'

        if re.fullmatch(regex, interval) is None:
            raise ValueError(f'Invalid interval: {interval}')


    def _ParseInterval(self):
        intervalStr = self._RawConfig['Interval']

        seconds = self._ParseIntervalComponent(intervalStr, 's')
        minutes = self._ParseIntervalComponent(intervalStr, 'm')
        hours   = self._ParseIntervalComponent(intervalStr, 'h')

        minutes += hours * 60
        seconds += minutes * 60

        self._Config.Interval = seconds


    def _ParseIntervalComponent(self, interval_str, component):
        match = re.search(rf'([0-9.]+){component}', interval_str)

        return float(match.group(1)) if match is not None else 0.
