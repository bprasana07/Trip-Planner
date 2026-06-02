
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

class ServiceStatus:
    """
    Class for registering and reporting overall status of the service,
    primarily for interaction with external deployment environment.
    """

    def __init__(self, service_name: str):
        """
        Constructor.
        """
        self.service_name: str = service_name
        self.service_requested: bool = True
        self.service_ready: bool = False

    def set_status(self, status: bool):
        """
        Set the status of a service
        """
        self.service_ready = status

    def is_ready(self) -> bool:
        """
        True if service is ready
        """
        return self.service_ready

    def set_requested(self, requested: bool):
        """
        Set if a service is requested by neuro-san server.
        """
        self.service_requested = requested

    def is_requested(self) -> bool:
        """
        True if service is requested.
        """
        return self.service_requested

    def get_service_name(self) -> str:
        """
        Return service name
        """
        return self.service_name
