
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

logger = Logger(level=logging.INFO)


class PseudowireProvider(object):

    def __init__(self, **args):
        pass

    # Methods to support creation
    #
    # Returns: handle
    #
    def create(self, port1, port2, vlanid, pseudowireservice):
        # Default method needs to be overriden
        logger.info("create called - should be overriden")

    # Method to support connection
    #
    def connect(self, handle):
        # Default method needs to be overriden
        logger.info("connect called - should be overriden")
        return None

    # Method to support disconnection
    #
    def disconnect(self, handle):
        # Default method needs to be overriden
        logger.info("discoconnect called - should be overriden")

    # Methods to support deletion
    #
    def delete(self, handle):
        # Default method needs to be overriden
        logger.info("delete called - should be overriden")