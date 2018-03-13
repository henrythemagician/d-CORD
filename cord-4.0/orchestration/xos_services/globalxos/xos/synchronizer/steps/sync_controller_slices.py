
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


import os
import base64
from collections import defaultdict
from netaddr import IPAddress, IPNetwork
from django.db.models import F, Q
from xos.config import Config
from synchronizers.base.syncstep import *
from core.models import *
from synchronizers.base.ansible_helper import *
from xos.logger import observer_logger as logger
import json

class SyncControllerSlices(SyncStep):
    provides=[Slice]
    requested_interval=0
    observes=ControllerSlice
    playbook='sync_controller_slices.yaml'

    def map_sync_inputs(self, controller_slice):
        logger.info("sync'ing slice controller %s" % controller_slice)

        if not controller_slice.controller.admin_user:
            logger.info("controller %r has no admin_user, skipping" % controller_slice.controller)
            return

        controller_users = ControllerUser.objects.filter(user=controller_slice.slice.creator,
                                                             controller=controller_slice.controller)
        if not controller_users:
            raise Exception("slice creator %s has not account at controller %s" % (controller_slice.slice.creator, controller_slice.controller.name))
        else:
            controller_user = controller_users[0]

        max_instances=int(controller_slice.slice.max_instances)
        slice_fields = {
            'endpoint': controller_slice.controller.auth_url,
            'admin_user': controller_slice.controller.admin_user,
            'admin_password': controller_slice.controller.admin_password,
            'slice_name': controller_slice.slice.name,
            'slice_description': controller_slice.slice.description,
            'name': controller_user.user.email,
            'ansible_tag': '%s@%s'%(controller_slice.slice.name,controller_slice.controller.name),
            'image': controller_slice.slice.default_image.name,
            'addresses': '10.168.2.0/24',          # FIXME
            'gateway_ip': '10.168.2.1',            # FIXME
            'gateway_mac': '02:42:0a:a8:02:01',    # FIXME
            'max_instances': max_instances
        }

        return slice_fields

    def map_sync_outputs(self, controller_slice, res):
        if (not controller_slice.tenant_id):
            controller_slice.tenant_id = "Not implemented"
            controller_slice.backend_status = '1 - OK'
            controller_slice.save()


    def map_delete_inputs(self, controller_slice):
        controller_users = ControllerUser.objects.filter(user=controller_slice.slice.creator,
                                                              controller=controller_slice.controller)
        if not controller_users:
            raise Exception("slice creator %s has not account at controller %s" % (controller_slice.slice.creator, controller_slice.controller.name))
        else:
            controller_user = controller_users[0]

        slice_fields = {
            'endpoint': controller_slice.controller.auth_url,
            'admin_user': controller_slice.controller.admin_user,
            'admin_password': controller_slice.controller.admin_password,
            'slice': controller_slice.slice.name,
            'slice_description': controller_slice.slice.description,
            'name': controller_user.user.email,
            'ansible_tag': '%s@%s'%(controller_slice.slice.name,controller_slice.controller.name),
            'delete': True
        }
	return slice_fields
