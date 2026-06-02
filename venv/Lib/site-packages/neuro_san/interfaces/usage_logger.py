
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


class UsageLogger:
    """
    Interface for logging per-user usage statistics.

    The idea here is that employing an implementation of one of these
    for any given Neuro SAN server is completely optional.
    """

    async def log_usage(self, token_dict: Dict[str, Any], request_metadata: Dict[str, Any]):
        """
        Logs the token usage for external capture.

        :param token_dict: A dictionary that describes overall token usage for a completed request.

                For each class of LLM (more or less equivalent to an LLM provider), there will
                be one key whose value is a dictionary with some other keys:

                Relevant keys include:
                    "completion_tokens" - Integer number of tokens generated in response to LLM input
                    "prompt_tokens" - Integer number of tokens that provide input to an LLM
                    "time_taken_in_seconds" - Float describing the total wall-clock time taken for the request.
                    "total_cost" -  An estimation of the cost in USD of the request.
                                    This number is to be taken with a grain of salt, as these estimations
                                    can come from model costs from libraries instead of directly from
                                    providers.
                    "total_tokens" - Total tokens used for the request.

                More keys can appear, but should not be counted on.
                The ones listed above contain potentially salient information for usage logging purposes.

        :param request_metadata: A dictionary of filtered request metadata whose keys contain
                identifying information for the usage log.
        """
        raise NotImplementedError
