
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


class AgentNameMapper:
    """
    An abstract policy defining conversion
    between agent name as specified in a manifest file
    and a file path (relative to registry root directory) to this agent definition file.
    """

    def agent_name_to_filepath(self, agent_name: str) -> str:
        """
        Converts an agent name from manifest file to file path to this agent definition file.
        """
        raise NotImplementedError()

    def filepath_to_agent_network_name(self, filepath: str) -> str:
        """
        Converts a file path to agent definition file (relative to registry root directory)
        to agent network name identifying it to the service.
        """
        raise NotImplementedError()
