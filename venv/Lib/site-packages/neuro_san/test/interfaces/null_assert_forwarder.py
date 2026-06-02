
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

from neuro_san.test.interfaces.assert_forwarder import AssertForwarder


class NullAssertForwarder(AssertForwarder):
    """
    Implementation of the AssertForwarder interface that does nothing for each assert type.
    This is useful as a superclass for other AssertForwarders that only want to focus
    on a few specific asserts.
    """

    # pylint: disable=invalid-name
    def assertEqual(self, first: Any, second: Any, msg: str = None):
        """
        Assert that the first is equal to the second

        :param first: First comparison element
        :param second: Second comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertNotEqual(self, first: Any, second: Any, msg: str = None):
        """
        Assert that the first is not equal to the second

        :param first: First comparison element
        :param second: Second comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertTrue(self, expr: Any, msg: str = None):
        """
        Assert that the expression is true

        :param expr: Expression to test
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertFalse(self, expr: Any, msg: str = None):
        """
        Assert that the expression is false

        :param expr: Expression to test
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertIs(self, first: Any, second: Any, msg: str = None):
        """
        Assert that the first and second are the same object

        :param first: First comparison element
        :param second: Second comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertIsNot(self, first: Any, second: Any, msg: str = None):
        """
        Assert that the first and second are not the same object

        :param first: First comparison element
        :param second: Second comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertIsNone(self, expr: Any, msg: str = None):
        """
        Assert that the expression is None

        :param expr: Expression to test
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertIsNotNone(self, expr: Any, msg: str = None):
        """
        Assert that the expression is not None

        :param expr: Expression to test
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertIn(self, member: Any, container: Any, msg: str = None):
        """
        Assert that the member is in the container

        :param member: Member comparison element
        :param container: Container comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertNotIn(self, member: Any, container: Any, msg: str = None):
        """
        Assert that the member is not in the container

        :param member: Member comparison element
        :param container: Container comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertIsInstance(self, obj: Any, cls: Any, msg: str = None):
        """
        Assert that the obj is an instance of the cls

        :param obj: object instance comparison element
        :param cls: Class comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertNotIsInstance(self, obj: Any, cls: Any, msg: str = None):
        """
        Assert that the obj is not an instance of the cls

        :param obj: object instance comparison element
        :param cls: Class comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertGreater(self, first: Any, second: Any, msg: str = None):
        """
        Assert that the first is greater than the second.

        :param first: First comparison element
        :param second: Second comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertGreaterEqual(self, first: Any, second: Any, msg: str = None):
        """
        Assert that the first is greater than or equal to the second.

        :param first: First comparison element
        :param second: Second comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertLess(self, first: Any, second: Any, msg: str = None):
        """
        Assert that the first is less than the second.

        :param first: First comparison element
        :param second: Second comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertLessEqual(self, first: Any, second: Any, msg: str = None):
        """
        Assert that the first is less than or equal to the second.

        :param first: First comparison element
        :param second: Second comparison element
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertGist(self, gist: bool, acceptance_criteria: str, text_sample: str, msg: str = None):
        """
        Assert that the gist is true

        :param gist: Pass/Fail value of the gist expected to be True
        :param acceptance_criteria: The value to verify against
        :param text_sample: The value appearing in the test sample
        :param msg: optional string message
        """
        # Do nothing

    # pylint: disable=invalid-name
    def assertNotGist(self, gist: bool, acceptance_criteria: str, text_sample: str, msg: str = None):
        """
        Assert that the gist is true

        :param gist: Pass/Fail value of the gist expected to be False
        :param acceptance_criteria: The value to verify against
        :param text_sample: The value appearing in the test sample
        :param msg: optional string message
        """
        # Do nothing
