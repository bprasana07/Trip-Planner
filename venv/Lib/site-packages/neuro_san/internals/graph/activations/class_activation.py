
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


class ClassActivation(AbstractClassActivation):
    """
    A ClassActivation that retrieves the full class reference directly from the class specification
    in agent network hocon.
    """

    def get_full_class_ref(self) -> str:
        """
        Returns the full class reference path directly from the class specification.

        This implementation expects the fully qualified class name to be provided
        in the "class" field of the `agent_tool_spec` dictionary.

        :return: A dot-separated string representing the full class path.
        """
        return self.agent_tool_spec.get("class")
