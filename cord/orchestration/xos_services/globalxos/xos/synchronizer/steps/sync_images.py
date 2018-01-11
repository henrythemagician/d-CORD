
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
from django.db.models import F, Q
from xos.config import Config
from core.models.image import Image
from xos.logger import observer_logger as logger
from synchronizers.base.syncstep import *

class SyncImages(SyncStep):
    provides=[Image]
    requested_interval=0
    observes=Image

    # We're not sync'ing sites with L-XOS
    # Just mark it as sync'ed
    def sync_record(self, image):
        image.backend_status = "0 - not sync'ed by globalxos"
        image.save()
