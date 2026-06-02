
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

from os import environ

from leaf_common.config.resolver_util import ResolverUtil

from neuro_san.interfaces.usage_logger import UsageLogger
from neuro_san.service.usage.wrapped_usage_logger import WrappedUsageLogger


class UsageLoggerFactory:
    """
    Implementation of the UsageLogger interface that merely spits out
    usage stats to the logger.
    """

    @staticmethod
    def create_usage_logger() -> WrappedUsageLogger:
        """
        Reads the server environment variables to create a UsageLogger instance.

        :return: A WrappedUsageLogger that wraps the class referred to by the
                AGENT_USAGE_LOGGER env var.  Can throw an exception
                if there are problems creating the class referenced by the env var.
        """
        usage_logger_class_name: str = environ.get("AGENT_USAGE_LOGGER")
        usage_logger: UsageLogger = ResolverUtil.create_instance(usage_logger_class_name,
                                                                 "AGENT_USAGE_LOGGER env var",
                                                                 UsageLogger)
        wrapped: WrappedUsageLogger = WrappedUsageLogger(usage_logger)
        return wrapped
