import inject
from watchdog.events import FileSystemEventHandler

from IgnoreService import IgnoreService

class CustomEventHandler(FileSystemEventHandler):
    @inject.autoparams()
    def __init__(self, ignoreService: IgnoreService):
        super().__init__()

        self._IgnoreService = ignoreService

    def dispatch(self, event):
        destPathShouldBeIgnored = True

        if hasattr(event, 'dest_path'):
            destPathShouldBeIgnored = self._IgnoreService.ShouldBeIgnored(event.dest_path)

        srcPathShouldBeIgnored = self._IgnoreService.ShouldBeIgnored(event.src_path)

        if not (destPathShouldBeIgnored and srcPathShouldBeIgnored):
            return super().dispatch(event)
