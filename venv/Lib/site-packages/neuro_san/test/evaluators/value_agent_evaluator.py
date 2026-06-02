
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

from neuro_san.test.evaluators.abstract_agent_evaluator import AbstractAgentEvaluator


class ValueAgentEvaluator(AbstractAgentEvaluator):
    """
    AbstractAgentEvaluator implementation that looks for specific values in output.
    """

    def test_one(self, verify_value: Any, test_value: Any):
        """
        :param verify_value: The value to verify against
        :param test_value: The value appearing in the test sample
        """
        if self.negate:
            self.asserts.assertNotEqual(verify_value, test_value)
        else:
            self.asserts.assertEqual(verify_value, test_value)
