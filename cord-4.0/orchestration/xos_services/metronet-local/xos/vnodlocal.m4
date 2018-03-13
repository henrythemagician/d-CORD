
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


tosca_definitions_version: tosca_simple_yaml_1_0

# compile this with "m4 vnodlocal.m4 > vnodlocal.yaml"

# include macros
include(macros.m4)

node_types:
    
    tosca.nodes.VNodLocalService:
        derived_from: tosca.nodes.Root
        description: >
            CORD: The VNodLocal Service.
        capabilities:
            xos_base_service_caps
        properties:
            xos_base_props
            xos_base_service_props
            rest_hostname:
                type: string
                required: false
            rest_port:
                type: string
                required: false
            rest_user:
                type: string
                required: false
            rest_pass:
                type: string
                required: false