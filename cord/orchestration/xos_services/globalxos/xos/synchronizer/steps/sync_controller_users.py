
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
from core.models.site import Controller, SiteDeployment, SiteDeployment
from core.models.user import User
from core.models.controlleruser import ControllerUser
from synchronizers.base.ansible_helper import *
from xos.logger import observer_logger as logger
import json

class SyncControllerUsers(SyncStep):
    provides=[User]
    requested_interval=0
    observes=ControllerUser
    playbook='sync_controller_users.yaml'

    def map_sync_inputs(self, controller_user):
        if not controller_user.controller.admin_user:
            logger.info("controller %r has no admin_user, skipping" % controller_user.controller)
            return

        if not controller_user.user.site:
            raise Exception('Siteless user %s'%controller_user.user.email)

        if controller_user.user.email == controller_user.controller.admin_user:
            logger.info("user %s is the admin_user at controller %r, skipping" % (controller_user.user.email, controller_user.controller))
            return

        user_fields = {
            'endpoint':controller_user.controller.auth_url,
            'name': controller_user.user.email,
            'firstname': controller_user.user.firstname,
            'lastname': controller_user.user.lastname,
            'phone': controller_user.user.phone,
            'user_url': controller_user.user.user_url,
            'public_key': controller_user.user.public_key,
            'is_active': controller_user.user.is_active,
            'is_admin': controller_user.user.is_admin,
            'is_readonly': controller_user.user.is_readonly,
            'is_appuser': controller_user.user.is_appuser,
            'password': controller_user.user.remote_password,
            'admin_user': controller_user.controller.admin_user,
            'admin_password': controller_user.controller.admin_password,
            'ansible_tag':'%s@%s'%(controller_user.user.email.replace('@','-at-'),controller_user.controller.name),
        }
	return user_fields

    def map_sync_outputs(self, controller_user, res):
        #controller_user.kuser_id = res[0]['user']['id']
        controller_user.kuser_id = 'not implemented'
        controller_user.backend_status = '1 - OK'
        controller_user.save()

    def delete_record(self, controller_user):
        """
        if controller_user.kuser_id:
            driver = self.driver.admin_driver(controller=controller_user.controller)
            driver.delete_user(controller_user.kuser_id)
        """
        pass
