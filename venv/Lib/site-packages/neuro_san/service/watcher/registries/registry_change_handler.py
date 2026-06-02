
# Copyright © 2023-2026 Cognizant Technology Solutions Corp, www.cognizant.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# END COPYRIGHT

from typing import Dict
from typing import Tuple

import logging

from threading import Lock

from watchdog.events import FileSystemEventHandler


class RegistryChangeHandler(FileSystemEventHandler):
    """
    Class for handling watchdog events in server registry directory.
    """
    MODIFIED = "modified"
    CREATED = "created"
    DELETED = "deleted"

    def __init__(self):
        """
        Constructor.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.lock: Lock = Lock()
        self.event_counters: Dict[str, int] =\
            {RegistryChangeHandler.MODIFIED: 0,
             RegistryChangeHandler.CREATED: 0,
             RegistryChangeHandler.DELETED: 0}

    def on_modified(self, event):
        """
        Handler for modified registry files.
        """
        self.handle_event(RegistryChangeHandler.MODIFIED, event.src_path)

    def on_created(self, event):
        """
        Handler for created registry files.
        """
        self.handle_event(RegistryChangeHandler.CREATED, event.src_path)

    def on_deleted(self, event):
        """
        Handler for deleted registry files.
        """
        self.handle_event(RegistryChangeHandler.DELETED, event.src_path)

    def handle_event(self, event_name: str, src_path: str):
        """
        Handle general watchdog event.
        """
        if not self.filter_src_name(src_path):
            return
        with self.lock:
            self.event_counters[event_name] += 1
        self.logger.info("🔔 File %s: %s", event_name, src_path)

    def reset_event_counters(self) -> Tuple[int, int, int]:
        """
        Reset event counters and return current counters.
        """
        with self.lock:
            modified: int = self.event_counters[self.MODIFIED]
            added: int = self.event_counters[self.CREATED]
            deleted: int = self.event_counters[self.DELETED]
            self.event_counters =\
                {self.MODIFIED: 0,
                 self.CREATED: 0,
                 self.DELETED: 0}
        return modified, added, deleted

    def filter_src_name(self, src_name: str) -> bool:
        """
        Filter source names we are getting notifications for.
        :param src_name: file path we get notified about
        :return: True if we should consider this file path;
                 False otherwise.
        """
        if not src_name:
            return False
        if src_name.endswith(".hocon") or src_name.endswith(".json"):
            return True
        return False
