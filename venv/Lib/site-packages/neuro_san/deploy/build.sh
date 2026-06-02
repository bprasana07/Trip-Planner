#!/bin/bash -e

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

# Script used to build the container that runs the Decision Assistant Service
# Usage:
#   build.sh [--no-cache]
#
# The script must be run from the top-level directory of where your
# registries and code lives so as to properly import them into the Dockerfile.

export SERVICE_TAG=${SERVICE_TAG:-neuro-san}
export SERVICE_VERSION=${SERVICE_VERSION:-0.0.1}

function build_main() {
    # Outline function which delegates most work to other functions

    # Parse for a specific arg when debugging
    CACHE_OR_NO_CACHE="--rm"
    if [ "$1" == "--no-cache" ]
    then
        CACHE_OR_NO_CACHE="--no-cache --progress=plain"
    fi

    if [ -z "${TARGET_PLATFORM}" ]
    then
        TARGET_PLATFORM="linux/amd64"
    fi
    echo "Target Platform for Docker image generation: ${TARGET_PLATFORM}"

    DOCKERFILE=$(find . -name Dockerfile | sort | tail -1)

    # See if we are building from within neuro-san repo to optionally set a build arg.
    PACKAGE_INSTALL="DUMMY=dummy"
    if [ "$(ls -d neuro_san)" == "neuro_san" ]
    then
        PACKAGE_INSTALL="PACKAGE_INSTALL=/usr/local/neuro-san/myapp"
    fi
    echo "PACKAGE_INSTALL is ${PACKAGE_INSTALL}"

    # Build the docker image
    # DOCKER_BUILDKIT needed for secrets
    # shellcheck disable=SC2086
    DOCKER_BUILDKIT=1 docker build \
        -t neuro-san/${SERVICE_TAG}:${SERVICE_VERSION} \
        --platform ${TARGET_PLATFORM} \
        --build-arg NEURO_SAN_VERSION="${USER}-$(date +'%Y-%m-%d-%H-%M')" \
        --build-arg "${PACKAGE_INSTALL}" \
        -f "${DOCKERFILE}" \
        ${CACHE_OR_NO_CACHE} \
        .
}


# Call the build_main() outline function
build_main "$@"
