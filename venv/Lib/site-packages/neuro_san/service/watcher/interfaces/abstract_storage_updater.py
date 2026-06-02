
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

from neuro_san.service.watcher.interfaces.storage_updater import StorageUpdater


class AbstractStorageUpdater(StorageUpdater):
    """
    Abstract base class for StorageUpdater implementations for common policy
    about checking for when it is needed to do update_storage().
    """

    def __init__(self, update_period_in_seconds: int):
        """
        Constructor

        :param update_period_in_seconds: An int describing how long this instance
                ideally wants to go between calls to update_storage().
        """
        self.last_update: float = 0.0
        self.update_period_in_seconds: int = update_period_in_seconds

    def start(self):
        """
        Perform start up.
        """
        raise NotImplementedError

    def update_storage(self):
        """
        Perform an update
        """
        raise NotImplementedError

    def get_update_period_in_seconds(self) -> int:
        """
        :return: An int describing how long this instance ideally wants to go between
                calls to update_storage().
        """
        return self.update_period_in_seconds

    def needs_updating(self, time_now_in_seconds: float) -> bool:
        """
        :param time_now_in_seconds: The current time in seconds.
                    We expect this to be from time.time()
        :return: True if this instance needs updating. False otherwise.
        """
        update_period: int = self.get_update_period_in_seconds()
        if update_period <= 0:
            # Never
            return False

        next_update: float = self.last_update + float(update_period)
        if time_now_in_seconds < next_update:
            # Not yet
            return False

        self.last_update = time_now_in_seconds
        return True
