#!/usr/bin/env python
# (C) Copyright 2018 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools
import os

os.environ["PBR_VERSION"] = '1.0.0'
os.environ["SKIP_GIT_SDIST"] = '1'
os.environ["SKIP_GENERATE_AUTHORS"] = '1'
os.environ["SKIP_WRITE_GIT_CHANGELOG"] = '1'

setuptools.setup(
    setup_requires=['pbr'],
    pbr=True)
