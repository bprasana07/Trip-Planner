
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
from neuro_san.internals.errors.json_error_formatter import JsonErrorFormatter
from neuro_san.internals.errors.string_error_formatter import StringErrorFormatter
from neuro_san.internals.interfaces.error_formatter import ErrorFormatter


class ErrorFormatterFactory:
    """
    Factory class to create an appropriate ErrorFormatter
    """

    @staticmethod
    def create_formatter(name: str = "string") -> ErrorFormatter:
        """
        Creates an ErrorFormatter given the name.

        :param name: The name of the error formatter to use
        :return: An ErrorFormatter instance.
        """

        # Default
        formatter: ErrorFormatter = StringErrorFormatter()
        if name is None:
            return formatter

        if name.lower() == "json":
            formatter = JsonErrorFormatter()

        # When the need arises, we could conceivably add class name lookup
        # for error formatters here, not unlike the way we do for coded tools.

        return formatter
