
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
from typing import List
from typing import Union


class MetadataUtil:
    """
    Utilities to deal with metadata dictionaries.
    """

    @staticmethod
    def minimize_metadata(request_metadata: Dict[str, Any],
                          keys: Union[str, List[str]]) -> Dict[str, Any]:
        """
        :param request_metadata: The raw request metadata dictionary that could easily contain
                    more keys than we want to send to the UsageLogger.
        :param keys: The keys we want to send to the UsageLogger
                This can either be a single string with space-delimited keys, or a list of keys
        :return: A minimized dictionary that only sends the keys we need to the UsageLogger.
                The idea is that this prevents the UsageLogger from getting potentially
                sensitive information it shouldn't really have.

                If the requested keys in the metadata are not there, they will also not appear
                in the returned minimized dictionary.
        """
        minimized: Dict[str, Any] = {}

        if request_metadata is None:
            # No request data, nothing to fill
            return minimized

        # If there are no keys, there is nothing to fill.
        if not keys:
            return minimized

        keys_list: List[str] = []

        # Check if keys is a string or a list
        if isinstance(keys, str):
            keys_list = keys.split(" ")
        elif isinstance(keys, List):
            keys_list = keys

        for key in keys_list:

            if not key:
                # Skip any empty key split from the list. Allows for multi-spaces.
                continue

            value: str = request_metadata.get(key)
            if value:
                minimized[key] = value

        return minimized
