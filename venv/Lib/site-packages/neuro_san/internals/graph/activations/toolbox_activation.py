
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

from neuro_san.internals.graph.activations.abstract_class_activation import AbstractClassActivation
from neuro_san.internals.interfaces.context_type_toolbox_factory import ContextTypeToolboxFactory
from neuro_san.internals.interfaces.invocation_context import InvocationContext


class ToolboxActivation(AbstractClassActivation):
    """
    A ClassActivation that resolves the full class reference from a predefined coded tool in the toolbox.

    Note that this class does not apply to Langchain's base tools.
    """

    def get_full_class_ref(self) -> str:
        """
        Returns the full class reference path from a predefined toolbox.

        This implementation looks up the tool by name in a toolbox, using the
        "toolbox" field in `agent_tool_spec`, then determine the class of that
        coded tool.

        :return: A dot-separated string representing the full class path.
        """
        tool_name: str = self.agent_tool_spec.get("toolbox")
        invocation_context: InvocationContext = self.run_context.get_invocation_context()
        toolbox_factory: ContextTypeToolboxFactory = invocation_context.get_toolbox_factory()
        return toolbox_factory.get_shared_coded_tool_class(tool_name)
