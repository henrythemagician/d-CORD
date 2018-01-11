
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

import requests, json
from requests.auth import HTTPBasicAuth

logger = Logger(level=logging.INFO)

class SegmentRoutingVlanXconnectPseudowireProvider(PseudowireProvider):

    def __init__(self, **args):
        pass

    # Methods to support creation
    #
    # Returns: handle
    #
    def create(self, port1, port2, vlanid, pseudowireservice):
        # Create method - create xconnect
        # Vlan is TBD
        pseudowirename = ("port1: %s, port2: %s, vlan: %s" % (port1, port2, vlanid))
        logger.info("SegmentRoutingXConnect create called, name: %s" % pseudowirename )

        # Pull out Ports from FQN


        # Pull out Device from FQN
        # Use default user/password?

        # curl --user onos:rocks -X POST -H "Content-Type: application/json" http://138.120.151.126:8181/onos/v1/network/configuration/apps/org.onosproject.segmentrouting/xconnect -d '{ "of:0000000000000001" : [{"vlan" : "100", "ports" : [1, 2], "name" : "Mike"}] }'

        # Port 1 Device and Num
        port1IdToken = port1.split('/', 1)
        port1Devicename = port1IdToken[0]
        port1Num = port1IdToken[1]

        # Port 2 Device and Num
        port2IdToken = port2.split('/', 1)
        port2Devicename = port2IdToken[0]
        port2Num = port2IdToken[1]

        # Lets make sure the Devices are the same - otherwise its an error - Xconnect must be on same device

        if (port1Devicename != port2Devicename):
            Exception("XConnect Device must be the same. D1= % D2=%" % (port1Devicename, port2Devicename))

        # Get URL from PwaaS Ojbect
        restCtrlUrl = pseudowireservice.networkControllerUrl

        data = {
            port2Devicename : [
                {
                    "vlan" : vlanid,
                    "ports" : [port1Num, port2Num],
                    "name" : pseudowirename
                }
            ]
           }

        headers = {'Content-Type': 'application/json'}

        resp = requests.post('{}/v1/network/configuration/apps/org.onosproject.segmentrouting/xconnect'.format(restCtrlUrl),
                             data=json.dumps(data), headers=headers, auth=HTTPBasicAuth('karaf', 'karaf'))

        if resp.status_code == 200:
            logger.info("SegmentRoutingXConnect create successful")
            return pseudowirename
        else:
            Exception("Pseudowire create failed Error Code: %s" % resp.status_code)


    # Method to support connect
    #
    def connect(self, handle):
        # Connect method - this is a no-op for this module, it does not support a complext state machine
        logger.info("SegmentRoutingXConnect Pseudowire connect called, handle = %s" % handle)

    # Method to support disconnect connect
    #
    def disconnect(self, handle):
        # Disconnect method - impl is TBD
        logger.info("SegmentRoutingXConnect Pseudowire disconnect called, handle = %s" % handle)

        # Example command line syntax:
        # curl --user onos:rocks -X DELETE http://138.120.151.126:8181/onos/v1/network/configuration/apps/org.onosproject.segmentrouting/xconnect

    # Method to support deletion
    #
    def delete(self, handle):
        # Delete method - impl is TBD
        logger.info("SegmentRoutingXConnect Pseudowire delete called, handle = %s" % handle)


