
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

from leaf_common.config.config_filter_chain import ConfigFilterChain

from neuro_san.internals.graph.persistence.manifest_dict_config_filter import ManifestDictConfigFilter
from neuro_san.internals.graph.persistence.manifest_key_config_filter import ManifestKeyConfigFilter
from neuro_san.internals.graph.persistence.served_manifest_config_filter import ServedManifestConfigFilter


class ManifestFilterChain(ConfigFilterChain):
    """
    ConfigFilterChain for manifest files
    """

    def __init__(self, manifest_file: str):
        """
        Constructor

        :param manifest_file: The name of the manifest file we are processing for logging purposes
        """
        super().__init__()

        # Order matters
        self.register(ManifestKeyConfigFilter(manifest_file))
        self.register(ManifestDictConfigFilter(manifest_file))
        self.register(ServedManifestConfigFilter(manifest_file, warn_on_skip=True, entry_for_skipped=True))
