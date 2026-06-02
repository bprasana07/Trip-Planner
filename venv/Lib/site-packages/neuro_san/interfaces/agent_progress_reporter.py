
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
from typing import Any
from typing import Dict


class AgentProgressReporter:
    """
    An interface for CodedTools to be able to report on an agent network's progress.

    Instances get handed down via the CodedTool's arguments dictionary via the
    "progress_reporter" key via the invoke() or async_invoke() methods.

    Typically, progress is reported as a dictionary that is JSON-serializable
    and interpreted by the client on a per-agent-network basis in the structure.
    The simplest and most easily interpreted structure is simply to report a key of "progress"
    with a value of a float between 0.0 and 1.0, but other keys/values can be used to report
    (say) partial progress on a structure that is being built by the agent network so that it
    can be visualized by an in-the-know client.

    Text messages can also be sent as content, but more as differential comments.
    These are not recommended, as any given client may not be able to parse them very easily.
    """

    async def async_report_progress(self, structure: Dict[str, Any], content: str = ""):
        """
        Reports the structure and optional message to the chat message stream returned to the client
        To be used from within CodedTool.async_invoke().

        :param structure: The Dictionary instance to write as progress.
                        All keys and values must be JSON-serializable.
        :param content: An optional message to send to the client
        """
        raise NotImplementedError
