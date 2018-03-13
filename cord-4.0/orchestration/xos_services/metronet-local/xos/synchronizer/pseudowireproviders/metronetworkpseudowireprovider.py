
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


from xos.logger import Logger, logging
from synchronizers.vnodlocal.pseudowireproviders.pseudowireprovider import PseudowireProvider
from services.metronetwork.models import NetworkEdgeToEdgePointConnection, NetworkEdgePort

logger = Logger(level=logging.INFO)

class MetronetworkPseudowireProvider(PseudowireProvider):

    def __init__(self, **args):
        pass

    # Methods to support creation
    #
    # Returns: handle
    #
    def create(self, port1, port2, vlanid, psuedowireservice):
        # Create method - create eline with the ports
        # Vlan is TBD
        pseudowirename = ("Vlan: %s" % vlanid)
        logger.info("Metronetwork create called, name: %s" % pseudowirename )
        # Edge to Edge Point Connectivity creation
        edgetoedgeconnectivity = NetworkEdgeToEdgePointConnection()
        uni1port = NetworkEdgePort.objects.filter(pid__icontains=port1)
        if uni1port:
            uni1port = uni1port[0]
        uni2port = NetworkEdgePort.objects.filter(pid__icontains=port2)
        if uni2port:
            uni2port = uni2port[0]
        edgetoedgeconnectivity.uni1 = uni1port
        edgetoedgeconnectivity.uni2 = uni2port
        edgetoedgeconnectivity.vlanid = vlanid
        edgetoedgeconnectivity.type = 'Point_To_Point'
        edgetoedgeconnectivity.operstate = 'inactive'
        edgetoedgeconnectivity.adminstate = 'disabled'
        edgetoedgeconnectivity.name = pseudowirename
        edgetoedgeconnectivity.save()
        return pseudowirename

    # Method to support connect
    #
    def connect(self, handle):
        # Connect method - simply transition the state of the underlying object - the Metronet sync will do the rest
        logger.info("Metronetwork Pseudowire connect called, handle = %s" % handle)
        edgetoedgeconnectivity = NetworkEdgeToEdgePointConnection.objects.get(name=handle)
        edgetoedgeconnectivity.adminstate = 'activationrequested'
        edgetoedgeconnectivity.save()

    # Method to support disconnect connect
    #
    def disconnect(self, handle):
        # Connect method - simply transition the state of the underlying object - the Metronet sync will do the rest
        logger.info("Metronetwork Pseudowire disconnect called, handle = %s" % handle)
        edgetoedgeconnectivity = NetworkEdgeToEdgePointConnection.objects.get(name=handle)
        edgetoedgeconnectivity.adminstate = 'deactivationrequested'
        edgetoedgeconnectivity.save()

    # Method to support deletion
    #
    def delete(self, handle):
        # Delete method - simply set the state to deleted and the Metronet sync will do the rest
        logger.info("Metronetwork Pseudowire delete called, handle = %s" % handle)
        edgetoedgeconnectivity = NetworkEdgeToEdgePointConnection.objects.get(name=handle)
        edgetoedgeconnectivity.deleted = True
        edgetoedgeconnectivity.save()

