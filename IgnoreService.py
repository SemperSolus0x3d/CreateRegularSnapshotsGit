import os

class IgnoreService:
    def __init__(self):
        self._IgnorePatterns = None

    def GetIgnorePatterns(self):
        if self._IgnorePatterns is None:
            self.RefreshIgnorePatterns()

        return self._IgnorePatterns

    def RefreshIgnorePatterns(self):
        self._IgnorePatterns = self._GetIgnorePatternsForGitDir()

        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r', encoding='utf-8') as f:
                self._IgnorePatterns.extend((x.removesuffix('\n') for x in f.readlines()))


    def _GetIgnorePatternsForGitDir(self):
        # Watchdog uses pathlib.PurePath.match(),
        # which doesn't support ** in patterns, so
        # we have to use a dirty hack like this
        # to ignore .git folder

        MAX_GIT_DIR_DEPTH = 10

        patterns = []

        for i in range(MAX_GIT_DIR_DEPTH):
            pattern = '.git'

            for _ in range(i):
                pattern = os.path.join(pattern, '*')

            patterns.append(pattern)

        return patterns
