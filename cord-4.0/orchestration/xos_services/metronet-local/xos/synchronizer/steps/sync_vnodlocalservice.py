
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
import sys

from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible #if needed
from synchronizers.new_base.ansible_helper import run_template_ssh #if needed
from synchronizers.new_base.modelaccessor import *
import requests, json
from requests.auth import HTTPBasicAuth

from xos.logger import Logger, logging

# vnod local will be in steps/..
parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

logger = Logger(level=logging.INFO)


class SyncVnodLocalSystem(SyncStep):
    provides = [VnodLocalService]
    observes = VnodLocalService
    requested_interval = 0
    initialized = False

    def __init__(self, **args):
        SyncStep.__init__(self, **args)

    def fetch_pending(self, deletion=False):
        logger.info("VnodLocal fetch pending called")

        # Some comments to replace as we write the code

        #    The AdministrativeState state machine:
        #
        #               Diasabled (initial)
        #                    |
        #             ConfigurationRequested
        #             /      /            \
        #            /      /              \
        #      ConfigurationFailed      Configured---------DeactivationRequested
        #                                   \                      |
        #                         ActivationRequested              |
        #                         /      /        \                |
        #                        /      /          \               |
        #               ActivationFailed         Enabled -----------
        #
        #

        #  The  OperationalState state machine
        #
        #           active-----------------|
        #              |                   |
        #       inactivereported           |
        #              |                   |
        #          inactive----------activereported

        objs = []


        # The whole thing needs to be conditional on the VnodLocalSystem existing and being 'enabled'
        # This is the 'kill switch' in the system that is the first thing to check
        vnodlocalsystem = self.get_vnodlocal_system()

        if not vnodlocalsystem:
            logger.debug("No VnodLocal System Configured, skipping sync")
            return objs

        # Check to make sure the Metro Network System is enabled
        if vnodlocalsystem.administrativeState == 'disabled':
            # Nothing to do
            logger.debug("VnodLocal System configured - state is Disabled, skipping sync")
            return objs



        # Handle call when deletion is False
        if deletion is False:

            # First Part of Auto-attachement: What we need to do is ask the ECORD if there are any Spokes for our site
            # that are set to 'auto-attached' but are not currently actually attached
            # it will send back a list of servicehandles that meet that criteria. We will simply
            # check if we have already created a VnodLocal for that service handle, if we have do
            # nothing it should be still in progress. If we haven't create it, mark it as 'autoattached', set the
            # servicehandle and mark it as 'ConfigurationRequested'
            rest_url = vnodlocalsystem.restUrl
            sitename = vnodlocalsystem.name
            username = vnodlocalsystem.username
            password = vnodlocalsystem.password

            autoattachhandles = self.get_autoattachhandles(vnodlocalsystem)
            for autoattachhandle in autoattachhandles:
                # Check to see if it already exists - if not add it
                if not VnodLocalService.objects.filter(servicehandle=autoattachhandle).exists():
                    vnodlocal = VnodLocalService()
                    vnodlocal.servicehandle = autoattachhandle
                    vnodlocal.autoattached = True
                    vnodlocal.administrativeState = 'configurationrequested'
                    logger.debug("Adding Auto-attached VnodLocalService servicehandle: %s" % vnodlocal.servicehandle)
                    objs.append(vnodlocal)

            # Second Part of Auto-attachment
            # Look for auto-attachmed Services that are Configured, move them automaticaly to activationrequested
            autoattachconfigures = self.get_autoattachconfigured()
            for autoattachconfigure in autoattachconfigures:
                # Just bounce these forward to activationrequested to get them activated
                autoattachconfigure.administrativeState = 'activationrequested'
                objs.append(autoattachconfigure)


            # Check for admin status 'ConfigurationRequested'
            configreqs = VnodLocalService.objects.filter(administrativeState='configurationrequested')
            for configreq in configreqs:
                # Call the XOS Interface to configure the service
                logger.debug("Attempting to configure VnodLocalService servicehandle: %s" % configreq.servicehandle)
                # Add code to call REST api on the ECORD - For this state - we call VnodGlobal
                # with the servciehandle and sitename it
                # it gives us back the NNI port and Vlan Config
                # we then set our state to 'Configured' or 'ConfigurationFailed'
                servicehandle = configreq.servicehandle
                query = {"sitename": sitename, "servicehandle" : servicehandle}

                resp = requests.get("{}/vnodglobal_api_configuration/".format(rest_url), params=query,
                                    auth=HTTPBasicAuth(username, password))

                if resp.status_code == 200:
                    resp = resp.json()
                    # Success-path transitions to 'configured'
                    configreq.vlanid = resp['vlanid']
                    configreq.portid = resp['port']['name']
                    configreq.administrativeState = 'configured'

                    #update proxy adminstate in ecord
                    data = {"sitename": sitename, "servicehandle": servicehandle, "adminstate": 'configured',
                            "vlanid": configreq.vlanid, "portid": configreq.portid}
                    resp = requests.post("{}/vnodglobal_api_status/".format(rest_url), data=json.dumps(data),
                                     auth=HTTPBasicAuth(username, password))

                else:
                    configreq.administrativeState = 'configurationfailed'

                objs.append(configreq)


            # Check for admin status 'ActivationRequested'
            activationreqs = VnodLocalService.objects.filter(administrativeState='activationrequested')
            for acivationreq in activationreqs:
                # Call the XOS Interface to activate the service
                logger.debug("Attempting to activate VnodLocalService servicehandle: %s" % acivationreq.servicehandle)
                # Add code to call REST api on the ECORD - For this state we send the VnodGlobal
                # service our service handle, subscriber,
                # VnodLocalId (this id)
                # Once this is accepted we transition to the
                # Final state of 'Enabled' or 'ActivationFailed'
                servicehandle = acivationreq.servicehandle
                vnodlocalid = acivationreq.id
                vlanid = acivationreq.vlanid
                portid = acivationreq.portid

                data = {"sitename": sitename, "servicehandle": servicehandle, "vnodlocalid": vnodlocalid,
                        "vlanid": vlanid, "portid": portid, "activate": "true"}

                resp = requests.post("{}/vnodglobal_api_activation/".format(rest_url), data=json.dumps(data),
                                    auth=HTTPBasicAuth(username, password))

                if resp.status_code == 200:
                    # Success-path transitions to 'enabled'
                    acivationreq.administrativeState = 'enabled'

                    # update proxy adminstate in ecord
                    data = {"sitename": sitename, "servicehandle": servicehandle, "adminstate": 'enabled',
                            "vlanid": vlanid, "portid": portid, "operstate": "active"}
                    resp = requests.post("{}/vnodglobal_api_status/".format(rest_url), data=json.dumps(data),
                                         auth=HTTPBasicAuth(username, password))
                else:
                    acivationreq.administrativeState = 'activationfailed'

                    # update proxy adminstate in ecord
                    data = {"sitename": sitename, "servicehandle": servicehandle, "adminstate": 'impaired',
                            "operstate": "inactive", "vlanid": vlanid, "portid": portid}
                    resp = requests.post("{}/vnodglobal_api_status/".format(rest_url), data=json.dumps(data),
                                         auth=HTTPBasicAuth(username, password))

                objs.append(acivationreq)


            # Check for admin status 'DeactivationRequested'
            deactivationreqs = VnodLocalService.objects.filter(administrativeState='deactivationrequested')
            for deacivationreq in deactivationreqs:
                # Call the XOS Interface to de-actiavte the spoke
                logger.debug("Attempting to de-activate VnodLocalService servicehandle: %s" % deacivationreq.servicehandle)
                # Add code to call REST api on the ECORD - Report change to VnodGlobal
                servicehandle = deacivationreq.servicehandle
                vnodlocalid = deacivationreq.id
                vlanid = deacivationreq.vlanid
                portid = deacivationreq.portid


                data = {"sitename": sitename, "servicehandle": servicehandle, "vnodlocalid": vnodlocalid,
                        "vlanid": vlanid, "portid": portid, "activate": "false"}

                resp = requests.post("{}/vnodglobal_api_activation/".format(rest_url), data=json.dumps(data),
                                     auth=HTTPBasicAuth(username, password))

                if resp.status_code == 200:
                    # Success-path transitions to 'enabled'
                    deacivationreq.administrativeState = 'configured'
                else:
                    deacivationreq.administrativeState = 'deactivationfailed'

                # update proxy adminstate in ecord
                data = {"sitename": sitename, "servicehandle": servicehandle, "adminstate": 'impaired',
                        "vlanid": vlanid, "portid": portid}
                resp = requests.post("{}/vnodglobal_api_status/".format(rest_url), data=json.dumps(data),
                                     auth=HTTPBasicAuth(username, password))

                objs.append(deacivationreq)


            # Check for oper status inactive reported
            inactivereports = VnodLocalService.objects.filter(operstate='inactivereported')
            for inactivereport in inactivereports:
                # Call the XOS Interface to report operstate issue
                logger.debug("Attempting to report inactive VnodLocalService servicehandle: %s" % inactivereport.servicehandle)
                # Add code to call REST api on the ECORD - Report change to VnodGlobal

                servicehandle = inactivereport.servicehandle
                vlanid = inactivereport.vlanid
                portid = inactivereport.portid

                # update proxy operstate in ecord
                data = {"sitename": sitename, "servicehandle": servicehandle, "operstate": "inactive",
                        "adminstate":"impaired", "vlanid": vlanid, "portid": portid}
                resp = requests.post("{}/vnodglobal_api_status/".format(rest_url), data=json.dumps(data),
                                     auth=HTTPBasicAuth(username, password))

                # transition to 'inactive' state regardless of whether call to ECORD was successful?!?
                inactivereport.operstate = 'inactive'
                objs.append(inactivereport)


            # Check for oper status active reported
            activereports = VnodLocalService.objects.filter(operstate='activereported')
            for activereport in activereports:
                # Call the XOS Interface to report operstate issue
                logger.debug(
                    "Attempting to report active VnodLocalService servicehandle: %s" % activereport.servicehandle)

                servicehandle = activereport.servicehandle
                vlanid = activereport.vlanid
                portid = activereport.portid
                # Add code to call REST api on the ECORD - Report change to VnodGlobal.
                # update proxy operstate in ecord
                data = {"sitename": sitename, "servicehandle": servicehandle, "operstate": "active",
                        "vlanid": vlanid, "portid": portid}
                resp = requests.post("{}/vnodglobal_api_status/".format(rest_url), data=json.dumps(data),
                                 auth=HTTPBasicAuth(username, password))

                activereport.operstate = 'active'
                objs.append(activereport)
        elif deletion:
            # Apply Deletion Semantics:
            logger.debug("Applying Deletion Semanctics")
            # TODO: Figure out the odd scenario of Service deletion
            deletedobjs = VnodLocalService.deleted_objects.all()
            objs.extend(deletedobjs)

        # Finally just return the set of changed objects
        return objs

    def get_vnodlocal_system(self):
        # We only expect to have one of these objects in the system in the curent design
        # So get the first element from the query
        vnodlocalsystems = VnodLocalSystem.objects.all()
        if not vnodlocalsystems:
            return None

        return vnodlocalsystems[0]

    def get_autoattachhandles(self, vnodlocalsystem):
        # Figure out API call to actually get this to work
        rest_url = vnodlocalsystem.restUrl
        sitename = vnodlocalsystem.name
        username=vnodlocalsystem.username
        password=vnodlocalsystem.password
        query = {"sitename":sitename}


        resp = requests.get("{}/vnodglobal_api_autoattach/".format(rest_url), params=query,
                            auth=HTTPBasicAuth(username, password))

        handles = []
        if resp.status_code == 200:
            resp = resp.json()
            handles = resp['servicehandles']
        else:
            logger.debug("Request for autoattach servicehandles failed.")

        return handles

    def get_autoattachconfigured(self):
        # Query for the set of auto-attached handles that are  in the 'Configured' state
        autoattachedconfigured = VnodLocalService.objects.filter(autoattached=True, administrativeState='configured')

        if not autoattachedconfigured:
            return []

        return autoattachedconfigured


    def sync_record(self, o):

        # Simply save the record to the DB - both updates and adds are handled the same way
        o.save()


    def delete_record(self, o):
        # Overriden to customize our behaviour - the core sync step for will remove the record directly
        # We just log and return
        logger.debug("deleting Object %s" % str(o), extra=o.tologdict())

