
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
from django.db.models import F, Q
from xos.config import Config
from synchronizers.base.syncstep import *
from core.models.slice import Controller, SlicePrivilege
from core.models.user import User
from core.models.controlleruser import ControllerUser, ControllerSlicePrivilege
from synchronizers.base.ansible_helper import *
from xos.logger import observer_logger as logger
import json

class SyncControllerSlicePrivileges(SyncStep):
    provides=[SlicePrivilege]
    requested_interval=0
    observes=ControllerSlicePrivilege
    playbook = 'sync_controller_slice_privileges.yaml'

    def map_sync_inputs(self, controller_slice_privilege):
        if not controller_slice_privilege.controller.admin_user:
            logger.info("controller %r has no admin_user, skipping" % controller_slice_privilege.controller)
            return

        template = os_template_env.get_template('sync_controller_users.yaml')
        role = controller_slice_privilege.slice_privilege.role.role
	# setup user home slice roles at controller
        if not controller_slice_privilege.slice_privilege.user.site:
            raise Exception('Sliceless user %s'%controller_slice_privilege.slice_privilege.user.email)
        user_fields = {
           'endpoint':controller_slice_privilege.controller.auth_url,
		   'user_name': controller_slice_privilege.slice_privilege.user.email,
           'admin_user': controller_slice_privilege.controller.admin_user,
		   'admin_password': controller_slice_privilege.controller.admin_password,
           'ansible_tag':'%s@%s@%s'%(controller_slice_privilege.slice_privilege.user.email.replace('@','-at-'),controller_slice_privilege.slice_privilege.slice.name,controller_slice_privilege.controller.name),
		   'role':role,
		   'slice_name':controller_slice_privilege.slice_privilege.slice.name}
        return user_fields

    def map_sync_outputs(self, controller_slice_privilege, res):
        controller_slice_privilege.role_id = res[0]['id']
        controller_slice_privilege.save()

    def delete_record(self, controller_slice_privilege):
        controller_register = json.loads(controller_slice_privilege.controller.backend_register)
        if (controller_register.get('disabled',False)):
            raise InnocuousException('Controller %s is disabled'%controller_slice_privilege.controller.name)
