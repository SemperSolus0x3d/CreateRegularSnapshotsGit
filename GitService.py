import os
import subprocess as sp
from threading import Lock
from datetime import datetime

class GitService:
    def __init__(self):
        self._Lock = Lock()


    def AddFiles(self, *files):
        self._EnsureRepoExists()
        self._TryCallGit([
            'add', *files
        ])


    def Commit(self, message=None):
        self._EnsureRepoExists()
        self._CallGit([
            'commit', '-m', self._GetCommitMessage(message)
        ])


    def _CallGit(self, args: list[str]):
        if not self._TryCallGit(args):
            raise Exception('Git call failed')


    def _TryCallGit(self, args: list[str]) -> bool:
        with self._Lock:
            returncode = sp.Popen(['git', *args]).wait()

            return returncode == 0


    def _GetCommitMessage(self, message=None):
        datetimeStr = datetime.strftime(
            datetime.now(),
            '%Y-%m-%d_%H-%M-%S.%f'
        )

        commitMessage = f'[{datetimeStr}]'

        if message is not None:
            commitMessage += ' ' + message

        return commitMessage

    def _EnsureRepoExists(self):
        if not os.path.exists('.git'):
            self._CallGit(['init'])
