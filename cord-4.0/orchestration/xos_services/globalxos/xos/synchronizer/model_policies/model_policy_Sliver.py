
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



def handle(instance):
    from core.models import Controller, ControllerSlice, ControllerNetwork, NetworkSlice

    networks = [ns.network for ns in NetworkSlice.objects.filter(slice=instance.slice)]
    controller_networks = ControllerNetwork.objects.filter(network__in=networks,
                                                                controller=instance.node.site_deployment.controller)

    for cn in controller_networks:
        if (cn.lazy_blocked):	
		cn.lazy_blocked=False
		cn.backend_register = '{}'
		cn.save()
