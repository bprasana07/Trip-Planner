#!/bin/bash

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

# Usage: ./convert_yaml_to_json.sh input.yaml output.json

INPUT="$1"
OUTPUT="$2"

if [[ -z "$INPUT" || -z "$OUTPUT" ]]; then
  echo "❗ Usage: $0 input.yaml output.json"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "❌ File not found: $INPUT"
  exit 1
fi

echo "🔄 Converting $INPUT → $OUTPUT..."

if command -v python3 &>/dev/null; then
  echo "Using Python..."
  python3 - <<EOF
import sys, json, yaml
with open("$INPUT") as f:
    data = yaml.safe_load(f)
with open("$OUTPUT", "w") as f:
    json.dump(data, f, indent=2)
EOF
else
  echo "❌ 'python3' is not available. Please install it."
  exit 1
fi

echo "✅ Done! Output saved to $OUTPUT"
