import os
import re
import fnmatch
import platform
import gitignorant as gi

class IgnoreService:
    def __init__(self):
        self._GitDirRegex = re.compile(fnmatch.translate(f'.git{os.sep}**'))
        self._GitignoreRules = None
        self._GitignoreExists: bool = None

    def RefreshPatterns(self):
        self._GitignoreExists = os.path.exists('.gitignore')

        if not self._GitignoreExists:
            self._GitignoreRules = []
            return

        with open('.gitignore', 'r', encoding='utf-8') as f:
            self._GitignoreRules = list(gi.parse_gitignore_file(f))


    def ShouldBeIgnored(self, path):
        self._RefreshPatternsIfNeeded()

        path = self._TransformPath(path)

        if path == '.git':
            return True

        if self._GitDirRegex.match(path):
            return True

        if not self._GitignoreExists:
            return False

        return gi.check_path_match(self._GitignoreRules, path)


    def _RefreshPatternsIfNeeded(self):
        if self._GitignoreRules is None:
            self.RefreshPatterns()


    def _ConvertDosDevicePathToTraditionalPath(self, path: str):
        if platform.system() != 'Windows':
            return path

        return path \
            .removeprefix('\\\\.\\') \
            .removeprefix('\\\\?\\')

    def _RemovePrefix(self, path: str):
        return path.removeprefix(f'.{os.sep}')

    def _TransformPath(self, path):
        traditionalPath = self._ConvertDosDevicePathToTraditionalPath(path)
        unprefixedPath = self._RemovePrefix(traditionalPath)

        return unprefixedPath
