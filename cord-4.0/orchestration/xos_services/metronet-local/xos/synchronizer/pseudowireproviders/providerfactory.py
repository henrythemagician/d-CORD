
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


import sys

from services.vnodlocal.models import VnodLocalSystem
from synchronizers.vnodlocal.pseudowireproviders.metronetworkpseudowireprovider import MetronetworkPseudowireProvider
from synchronizers.vnodlocal.pseudowireproviders.segmentroutingvlanxconnectpseudowireprovider import SegmentRoutingVlanXconnectPseudowireProvider


class ProviderFactory(object):
    @staticmethod
    def getprovider():

        # We look up the VnodLocal Configuration to see what to do
        vnodlocalsystems = VnodLocalSystem.objects.all()
        if not vnodlocalsystems:
            return None

        vnodlocalsystem = vnodlocalsystems[0]

        if vnodlocalsystem.pseudowireprovider == 'metronetwork':
            return MetronetworkPseudowireProvider()
        elif vnodlocalsystem.pseudowireprovider == 'segmentroutingxconnect':
            return SegmentRoutingVlanXconnectPseudowireProvider()
        else:
            return None