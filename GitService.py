import os
import subprocess as sp
from threading import Lock
from datetime import datetime

class GitService:
    def __init__(self):
        self._Lock = Lock()


    def AddFiles(self, *files):
        with self._Lock:
            self._EnsureRepoExists()
            self._TryCallGit([
                'add', *files
            ])


    def Commit(self, message=None):
        with self._Lock:
            self._EnsureRepoExists()

            if self._CheckForStagedChanges():
                self._CallGit([
                    'commit', '-m', self._GetCommitMessage(message)
                ])

                print('Created snapshot')


    def _CallGit(self, args: list[str]):
        if self._TryCallGit(args) != 0:
            raise Exception('Git call failed')


    def _TryCallGit(self, args: list[str]) -> int:
        return sp.Popen(['git', *args]).wait()


    def _CheckForStagedChanges(self) -> bool:
        return self._TryCallGit([
            'diff', '--staged', '--exit-code', '--color-words'
        ]) == 1


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
