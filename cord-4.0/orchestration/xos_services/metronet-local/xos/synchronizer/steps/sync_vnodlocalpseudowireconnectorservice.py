
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

from synchronizers.base.syncstep import SyncStep
from synchronizers.vnodlocal.pseudowireproviders.providerfactory import ProviderFactory
from services.vnodlocal.models import *

from xos.logger import Logger, logging

# vnod local will be in steps/..
parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

logger = Logger(level=logging.INFO)


class SyncVnodLocalPseudowireConnectorServiceSystem(SyncStep):
    provides = [VnodLocalPseudowireConnectorService]
    observes = VnodLocalPseudowireConnectorService
    requested_interval = 0
    initialized = False

    def __init__(self, **args):
        SyncStep.__init__(self, **args)

    def fetch_pending(self, deletion=False):
        logger.info("VnodLocalPseudowireConnector fetch pending called")

        # Some comments to replace as we write the code

        #    The AdministrativeState state machine:
        #
        #
        #                     Disabled---------DeactivationRequested
        #                         \                      |
        #               ActivationRequested              |
        #               /      /        \                |
        #              /      /          \               |
        #     ActivationFailed         Enabled -----------
        #
        #

        #  The  OperationalState state machine
        #
        #           active
        #              |
        #          inactive

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

            # Check for admin status 'ActivationRequested'
            activationreqs = VnodLocalPseudowireConnectorService.objects.filter(administrativeState='activationrequested')
            for activationreq in activationreqs:
                # Handle the case where we don't yet have a VnodLocalSerive
                if activationreq.vnodlocal is None:
                    # Create VnodLocalService
                    # We save the changes right here in this case to avoid having to to 'pre-save' semnatics
                    # to cover the foreign key
                    vnodlocalservice = VnodLocalService()
                    vnodlocalservice.servicehandle = activationreq.servicehandle
                    vnodlocalservice.administrativeState = 'configurationrequested'
                    vnodlocalservice.save()
                    activationreq.vnodlocal = vnodlocalservice
                    activationreq.save()
                elif activationreq.vnodlocal.administrativeState == 'configured':
                    # Once the underlying VnodLocal is configured then activated it
                    vnodlocalservice = activationreq.vnodlocal
                    # Call our underlying provider to connect the pseudo wire
                    self.activate_pseudowire(activationreq, vnodlocalsystem)
                    activationreq.administrativeState = 'enabled'
                    activationreq.operstate = 'active'
                    objs.append(activationreq)
                    vnodlocalservice.administrativeState = 'activationrequested'
                    vnodlocalservice.operstate = 'activereported'
                    objs.append(vnodlocalservice)


            # Check for admin status 'DeactivationRequested'
            deactivationreqs = VnodLocalPseudowireConnectorService.objects.filter(administrativeState='deactivationrequested')
            for deactivationreq in deactivationreqs:
                # Call the XOS Interface to de-actiavte the spoke
                logger.debug("Attempting to de-activate VnodLocalService servicehandle: %s" % deactivationreq.servicehandle)
                # De-activate the underlying service
                vnodlocalservice = deactivationreq.vnodlocal
                # Call our underlying provider to connect the pseudo wire
                self.deactivate_pseudowire(deactivationreq)
                deactivationreq.administrativeState = 'disabled'
                deactivationreq.operstate = 'inactive'
                objs.append(deactivationreq)
                vnodlocalservice.administrativeState = 'deactivationrequested'
                objs.append(vnodlocalservice)


        elif deletion:
            # Apply Deletion Semantics:
            logger.debug("Applying Deletion Semanctics")
            # TODO: Figure out the odd scenario of Service deletion
            deletedobjs = VnodLocalPseudowireConnectorService.deleted_objects.all()

            # Delete the underlying VnodLocalService objects
            for deletedobj in deletedobjs:
                # Set the VnodLocal to Deleted - its Synchronizer will take care of deletion
                vnodlocalobj = deletedobj.vnodlocal
                vnodlocalobj.deleted = True
                vnodlocalobj.save()
                # Delete the underlying pseudowire
                self.delete_pseudowire(deletedobj)
                # Finally - add the Service for deletion
                objs.append(deletedobj)

        # Finally just return the set of changed objects
        return objs


    def sync_record(self, o):

        # Simply save the record to the DB - both updates and adds are handled the same way
        o.save()


    def delete_record(self, o):
        # Overriden to customize our behaviour - the core sync step for will remove the record directly
        # We just log and return
        logger.debug("deleting Object %s" % str(o), extra=o.tologdict())

    def get_vnodlocal_system(self):
        # We only expect to have one of these objects in the system in the curent design
        # So get the first element from the query
        vnodlocalsystems = VnodLocalSystem.objects.all()
        if not vnodlocalsystems:
            return None

        return vnodlocalsystems[0]

    def activate_pseudowire(self, o, vnodlocalsystem):
        # Call the underlying pseudowire provicers and call
        logger.debug("activating pseudowire %s" % o.servicehandle)

        pseudowireprovier = ProviderFactory.getprovider()

        if pseudowireprovier is not None:
            # Pass it the two ports - the internal port configured on the Pseudowire and the NNI port from
            # the VnodLocal
            if o.pseudowirehandle == '':
                o.pseudowirehandle = pseudowireprovier.create(o.internalport, o.vnodlocal.portid, o.vnodlocal.vlanid, vnodlocalsystem)

            # handle already exists - just connect it
            pseudowireprovier.connect(o.pseudowirehandle)
        else:
            # No Provider configured - lets put a handle that reflects thsi
            o.pseudowirehandle = 'No Pseudowire Provider configured'


    def deactivate_pseudowire(self, o):
        # Call the underlying pseudowire provicers and call
        logger.debug("deactivating pseudowire %s" % o.servicehandle)

        pseudowireprovier = ProviderFactory.getprovider()

        if pseudowireprovier is not None:
            # Pass it the handle
            pseudowireprovier.disconnect(o.pseudowirehandle)


    def delete_pseudowire(self, o):
        # Call the underlying pseudowire provicers and call
        logger.debug("deleting pseudowire %s" % o.servicehandle)

        pseudowireprovier = ProviderFactory.getprovider()

        if pseudowireprovier is not None:
            # Pass it the handle
            if o.pseudowirehandle != '':
                pseudowireprovier.delete(o.pseudowirehandle)

        # Either way blank out the handle name
        o.pseudowirehandle = ''
