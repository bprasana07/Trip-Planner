
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

from neuro_san.internals.interfaces.context_type_toolbox_factory import ContextTypeToolboxFactory
from neuro_san.internals.run_context.factory.master_llm_factory import MasterLlmFactory
from neuro_san.internals.run_context.langchain.toolbox.toolbox_factory import ToolboxFactory


class MasterToolboxFactory:
    """
    Creates the correct kind of ContextTypeToolboxFactory
    """

    @staticmethod
    def create_toolbox_factory(config: Dict[str, Any] = None) -> ContextTypeToolboxFactory:
        """
        Creates an appropriate ContextTypeToolboxFactory

        :param config: The config dictionary which may or may not contain
                       keys for the context_type and default toolbox_config
        :return: A ContextTypeToolboxFactory appropriate for the context_type in the config.
        """

        toolbox_factory: ContextTypeToolboxFactory = None
        context_type: str = MasterLlmFactory.get_context_type(config)

        if context_type.startswith("openai"):
            toolbox_factory = None
        elif context_type.startswith("langchain"):
            toolbox_factory = ToolboxFactory(config)
        else:
            # Default case
            toolbox_factory = ToolboxFactory(config)

        return toolbox_factory
