import os
from fnmatch import fnmatchcase
import platform

class IgnoreService:
    def __init__(self):
        self._IgnorePatterns = None
        self._ForceIncludePatterns = None
        self._GitDirPattern = self._AdaptPatternToCurrentPlatform('./.git/**')

    def RefreshPatterns(self):
        self._IgnorePatterns = []
        self._ForceIncludePatterns = []

        if os.path.exists('.gitignore'):
            with open('.gitignore', 'r', encoding='utf-8') as f:
                allPatterns = (x.removesuffix('\n') for x in f.readlines())

            self._IgnorePatterns = self._TransformPatterns((
                x for x in allPatterns
                if not x.startswith('!')
            ))

            self._ForceIncludePatterns = self._TransformPatterns((
                x.removeprefix('!')
                for x in allPatterns
                if x.startswith('!')
            ))


    def ShouldBeIgnored(self, path):
        self._RefreshPatternsIfNeeded()

        if path == '.\\.git' or path == './.git':
            return True

        if fnmatchcase(path, self._GitDirPattern):
            return True

        if any((fnmatchcase(path, x) for x in self._ForceIncludePatterns)):
            return False

        return any((fnmatchcase(path, x) for x in self._IgnorePatterns))


    def _RefreshPatternsIfNeeded(self):
        if (
            self._IgnorePatterns is None or
            self._ForceIncludePatterns is None
        ):
            self.RefreshPatterns()

    def _AdaptPatternToCurrentPlatform(self, pattern: str):
        if platform.system() == 'Windows':
            return pattern.replace('/', '\\')
        else:
            return pattern

    def _AddPrefixToPattern(self, pattern: str):
        if not pattern.startswith('./'):
            return './' + pattern
        else:
            return pattern

    def _TransformPatterns(self, patterns):
        withPrefix = (self._AddPrefixToPattern(x) for x in patterns)
        adapted = (self._AdaptPatternToCurrentPlatform(x) for x in withPrefix)

        return list(adapted)
