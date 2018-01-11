
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


def handle(user):
    from core.models import Controller, ControllerSite, ControllerUser, User
    from collections import defaultdict

    # user = User.get(user_id)
    
    controller_users = ControllerUser.objects.filter(user=user)
    existing_controllers = [cu.controller for cu in controller_users]
    all_controllers = Controller.objects.all()
    for controller in all_controllers:
        if controller not in existing_controllers:
            ctrl_user = ControllerUser(controller=controller, user=user)
            ctrl_user.save()  

