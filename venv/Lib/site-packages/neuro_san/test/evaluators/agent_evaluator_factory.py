
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

from typing import Dict
from typing import Tuple
from typing import Type

from neuro_san.test.evaluators.gist_agent_evaluator import GistAgentEvaluator
from neuro_san.test.evaluators.greater_agent_evaluator import GreaterAgentEvaluator
from neuro_san.test.evaluators.keywords_agent_evaluator import KeywordsAgentEvaluator
from neuro_san.test.evaluators.less_agent_evaluator import LessAgentEvaluator
from neuro_san.test.evaluators.value_agent_evaluator import ValueAgentEvaluator
from neuro_san.test.interfaces.agent_evaluator import AgentEvaluator
from neuro_san.test.interfaces.assert_forwarder import AssertForwarder


class AgentEvaluatorFactory:
    """
    Factory that creates AgentEvaluators
    """

    NAME_TO_AGENT_EVALUATOR: Dict[str, Tuple[Type[AgentEvaluator], bool]] = {
        "gist": (GistAgentEvaluator, False),
        "not_gist": (GistAgentEvaluator, True),
        "greater": (GreaterAgentEvaluator, False),
        "not_greater": (GreaterAgentEvaluator, True),
        "keywords": (KeywordsAgentEvaluator, False),
        "not_keywords": (KeywordsAgentEvaluator, True),
        "less": (LessAgentEvaluator, False),
        "not_less": (LessAgentEvaluator, True),
        "value": (ValueAgentEvaluator, False),
        "not_value": (ValueAgentEvaluator, True),
    }

    @staticmethod
    def create_evaluator(asserts: AssertForwarder, evaluation_type: str) -> AgentEvaluator:
        """
        Creates AgentEvaluators

        :param asserts: The AssertForwarder instance to handle failures
        :param evaluation_type: A string key describing how the evaluation will take place
        """
        evaluator: AgentEvaluator = None

        # Return early
        if evaluation_type is None:
            return evaluator

        # Look up in the table
        lower_eval: str = evaluation_type.lower()
        eval_tuple: Tuple[Type[AgentEvaluator], bool] = AgentEvaluatorFactory.NAME_TO_AGENT_EVALUATOR.get(lower_eval)
        if eval_tuple is None:
            return evaluator

        # Get components of table value
        eval_class: Type[AgentEvaluator] = eval_tuple[0]
        negate: bool = eval_tuple[1]

        if negate is not None:
            evaluator = eval_class(asserts, negate=negate)
        else:
            evaluator = eval_class(asserts)

        return evaluator
