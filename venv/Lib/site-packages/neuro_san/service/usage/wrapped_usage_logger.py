
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

from asyncio import run
from os import environ

from neuro_san.interfaces.usage_logger import UsageLogger
from neuro_san.internals.utils.metadata_util import MetadataUtil


class WrappedUsageLogger(UsageLogger):
    """
    Implementation of the UsageLogger interface that wraps another UsageLogger
    and whose log_usage method makes sure sloppier inputs adhere better to the
    UsageLogger contract.
    """

    def __init__(self, wrapped: UsageLogger):
        """
        Constructor

        :param wrapped: The UsageLogger instance that is wrapped.
                        Can be None and log_usage() will handle that.
        """
        self.wrapped: UsageLogger = wrapped

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
        if self.wrapped is None:
            # Nothing to report
            return

        if token_dict is None:
            # Nothing to report
            return

        compliant_token_dict: Dict[str, Any] = self.make_compliant_token_dict(token_dict)

        # Try getting the value from the more specific env var before falling back to the
        # other env var.
        keys_string: str = environ.get("AGENT_USAGE_LOGGER_METADATA",
                                       environ.get("AGENT_FORWARDED_REQUEST_METADATA"))
        minimal_metadata: Dict[str, Any] = MetadataUtil.minimize_metadata(request_metadata, keys_string)

        await self.wrapped.log_usage(compliant_token_dict, minimal_metadata)

    def synchronous_log_usage(self, token_dict: Dict[str, Any], request_metadata: Dict[str, Any]):
        """
        Logs the token usage for external capture.
        See comments for log_usage() above.
        """
        run(self.log_usage(token_dict, request_metadata))

    def make_compliant_token_dict(self, token_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        :param token_dict: The token dictionary to make compliant if it is not already
        :return: A token dictionary compliant to the UsageLogger interface
        """
        compliant: Dict[str, Any] = token_dict

        if "total_tokens" in token_dict.keys():
            # We have a raw token dictionary without any attribution to the LLM.
            # Make the dictionary compliant
            compliant = {
                "all": token_dict
            }

        return compliant
