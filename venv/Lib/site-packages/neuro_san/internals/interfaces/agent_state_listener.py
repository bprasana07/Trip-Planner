
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

from neuro_san.internals.interfaces.agent_storage_source import AgentStorageSource


class AgentStateListener:
    """
    Abstract interface for publishing agent state changes -
    when an agent is being added or removed from the service.
    """

    def agent_added(self, agent_name: str, source: AgentStorageSource):
        """
        Agent is being added to the service.
        :param agent_name: name of an agent
        :param source: The AgentStorageSource source of the message
        """
        raise NotImplementedError

    def agent_modified(self, agent_name: str, source: AgentStorageSource):
        """
        Existing agent has been modified in service scope.
        :param agent_name: name of an agent
        :param source: The AgentStorageSource source of the message
        """
        raise NotImplementedError

    def agent_removed(self, agent_name: str, source: AgentStorageSource):
        """
        Agent is being removed from the service.
        :param agent_name: name of an agent
        :param source: The AgentStorageSource source of the message
        """
        raise NotImplementedError
