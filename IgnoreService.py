import os

class IgnoreService:
    def __init__(self):
        self._IgnorePatterns = None

    def GetIgnorePatterns(self):
        if self._IgnorePatterns is None:
            self.RefreshIgnorePatterns()

        return self._IgnorePatterns

    def RefreshIgnorePatterns(self):
        self._IgnorePatterns = ['.git']

        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r', encoding='utf-8') as f:
                self._IgnorePatterns.extend((x.removesuffix('\n') for x in f.readlines()))
