
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

from neuro_san.internals.interfaces.error_formatter import ErrorFormatter


class StringErrorFormatter(ErrorFormatter):
    """
    Implementation of ErrorFormatter interface which compiles error information
    into a string.   See parent interface for more details.
    """

    def format(self, agent_name: str, message: str, details: str = None) -> str:
        """
        Format an error message

        :param agent_name: A string describing the name of the agent experiencing
                the error.
        :param message: The specific message describing the error occurrence.
        :param details: An optional string describing further details of how/where the
                error occurred.  Think: traceback.
        :return: String encapsulation and/or filter of the error information
                presented in the arguments.
        """
        error: str = f"Error from {agent_name}: {message}"
        if details is not None:
            error = f"{error} ({details})"
        return error
