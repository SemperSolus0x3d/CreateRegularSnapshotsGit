import time
import os

import inject
from watchdog.observers import Observer
from watchdog.events import (
    DirMovedEvent,
    FileMovedEvent
)

from ConfigService import ConfigService
from GitService import GitService
from IgnoreService import IgnoreService
from CustomEventHandler import CustomEventHandler

class Program:
    @inject.autoparams()
    def __init__(
        self,
        configService: ConfigService,
        gitService: GitService,
        ignoreService: IgnoreService
    ):
        self._ConfigService = configService
        self._GitService = gitService
        self._IgnoreService = ignoreService
        self._FilesChanged = False


    def Main(self):
        self._GitService.AddFiles('.')
        self._FilesChanged = True

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
        eventHandler = CustomEventHandler()
        eventHandler.on_any_event = lambda e: self._OnAnyEvent(e)

        return eventHandler

    def _OnAnyEvent(self, event):
        if event.src_path == f'.{os.sep}.gitignore':
            self._IgnoreService.RefreshPatterns()

        if not self._IgnoreService.ShouldBeIgnored(event.src_path):
            self._GitService.AddFiles(event.src_path)
            self._FilesChanged = True

        if isinstance(event, (DirMovedEvent, FileMovedEvent)):
            if not self._IgnoreService.ShouldBeIgnored(event.dest_path):
                self._GitService.AddFiles(event.dest_path)
                self._FilesChanged = True


if __name__ == '__main__':
    try:
        inject.configure()
        Program().Main()
    except KeyboardInterrupt:
        print('Ctrl+C received. Exiting gracefully')
    except Exception as ex:
        print(ex)
        print('\a')
