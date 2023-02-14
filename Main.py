import time
from fnmatch import fnmatch

from watchdog.observers import Observer
from watchdog.events import (
    PatternMatchingEventHandler,
    DirMovedEvent,
    FileMovedEvent
)

from ConfigService import ConfigService
from GitService import GitService
from IgnoreService import IgnoreService

class Program:
    def __init__(self):
        self._ConfigService = ConfigService()
        self._GitService = GitService()
        self._IgnoreService = IgnoreService()
        self._FilesChanged = False


    def Main(self):
        self._GitService.AddFiles('.')

        config = self._ConfigService.GetConfig()
        eventHandler = self._GetEventHandler()
        observer = Observer()

        observer.schedule(
            eventHandler,
            '.',
            recursive=True
        )

        observer.start()

        try:
            while True:
                if self._FilesChanged:
                    self._GitService.Commit()
                    self._FilesChanged = False

                time.sleep(config.Interval)
        except Exception:
            observer.stop()
            observer.join()

            raise


    def _GetEventHandler(self):
        ignorePatterns = self._IgnoreService.GetIgnorePatterns()

        eventHandler = PatternMatchingEventHandler(
            None,
            ignorePatterns
        )

        eventHandler.on_any_event = lambda e: self._OnAnyEvent(e)

        return eventHandler


    def _ShouldBeIgnored(self, file) -> bool:
        patterns = self._IgnoreService.GetIgnorePatterns()

        return any((fnmatch(file, x) for x in patterns))


    def _OnAnyEvent(self, event):
        if not self._ShouldBeIgnored(event.src_path):
            self._GitService.AddFiles(event.src_path)
            self._FilesChanged = True

        if isinstance(event, (DirMovedEvent, FileMovedEvent)):
            if not self._ShouldBeIgnored(event.dest_path):
                self._GitService.AddFiles(event.dest_path)
                self._FilesChanged = True


if __name__ == '__main__':
    try:
        Program().Main()
    except KeyboardInterrupt:
        print('Ctrl+C received. Exiting gracefully')
    except Exception as ex:
        print(ex)
        print('\a')
