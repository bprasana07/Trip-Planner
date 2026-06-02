
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

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from datetime import tzinfo
from logging import getLogger
from logging import Logger
from zoneinfo import available_timezones
from zoneinfo import ZoneInfo

from neuro_san.interfaces.coded_tool import CodedTool


class GetCurrentDateTime(CodedTool):
    """
    CodedTool implementation which provides a current date and time for a given timezone.
    """

    async def async_invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> str:
        """
        :param args: An argument dictionary whose keys are the parameters
                to the coded tool and whose values are the values passed for them
                by the calling agent.  This dictionary is to be treated as read-only.

                The argument dictionary expects the following keys:
                    utc_offset: An integer representing the UTC offset in hours.
                    iana_timezone: A string representing the IANA timezone name.

        :param sly_data: A dictionary whose keys are defined by the agent hierarchy,
                but whose values are meant to be kept out of the chat stream.

                This dictionary is largely to be treated as read-only.
                It is possible to add key/value pairs to this dict that do not
                yet exist as a bulletin board, as long as the responsibility
                for which coded_tool publishes new entries is well understood
                by the agent chain implementation and the coded_tool implementation
                adding the data is not invoke()-ed more than once.

                Keys expected for this implementation are:
                    None

        :return:
            In case of successful execution:
                The current date and time of a given timezone as a string.
            otherwise:
                a text string an error message in the format:
                "Error: <error message>"
        """

        logger: Logger = getLogger(self.__class__.__name__)

        utc_offset: int = args.get("utc_offset")
        iana_timezone: str = args.get("iana_timezone", "UTC")

        # Try utc_offset first
        timezone_info: tzinfo = None
        if isinstance(utc_offset, int) and -24 < utc_offset < 24:
            try:
                timezone_info = timezone(timedelta(hours=utc_offset))
            except (TypeError, ValueError):
                pass

        # Fall back to iana_timezone if utc_offset failed
        if timezone_info is None and isinstance(iana_timezone, str) and iana_timezone in available_timezones():
            timezone_info = ZoneInfo(iana_timezone)

        # Return error only if both failed
        if timezone_info is None:
            error_msg: str = (
                "Error: Both timezone inputs are invalid. "
                "Please provide either a valid UTC offset (-24 to 24) or a valid IANA timezone "
                "(see https://www.iana.org/time-zones).\n"
                f"Got utc_offset: {utc_offset}, iana_timezone: {iana_timezone}."
            )
            logger.error(error_msg)
            return error_msg

        # Get current time for a given timezone
        now: datetime = datetime.now(timezone_info)

        # Format it in a user-friendly way
        friendly_time: str = now.strftime("%A, %B %d, %Y at %I:%M %p %Z")

        logger.debug("Current UTC date and time: %s", friendly_time)

        return str(now)
