
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


from core.admin import XOSBaseAdmin
from django.contrib import admin
from services.vnodlocal.models import *
from django import forms

class VnodLocalServiceAdmin(XOSBaseAdmin):
    verbose_name = "VNOD Local Service"
    verbose_name_plural = "VNOD Local Services"
    list_display = ('servicehandle', 'portid', 'vlanid', 'administrativeState', 'operstate', 'autoattached')
    list_display_links = ('servicehandle', 'portid', 'vlanid', 'administrativeState', 'operstate', 'autoattached')

    fields = ('id', 'servicehandle', 'portid', 'vlanid', 'administrativeState', 'operstate', 'autoattached')
    readonly_fields = ('id','autoattached')


class VnodLocalSystemAdminForm(forms.ModelForm):

    password = forms.CharField(required=False, widget = forms.PasswordInput(render_value=True))

    class Meta:
        model = VnodLocalSystem
        fields = '__all__'

class VnodLocalSystemAdmin(XOSBaseAdmin):
    verbose_name = "VNOD Local System"
    verbose_name_plural = "VNOD Local Systems"
    form = VnodLocalSystemAdminForm
    list_display = ('name', 'administrativeState', 'restUrl', 'username', 'pseudowireprovider', 'networkControllerUrl')
    list_display_links = ('name', 'administrativeState', 'restUrl', 'username', 'pseudowireprovider', 'networkControllerUrl')

    fields = ('name', 'administrativeState', 'restUrl', 'username', 'password', 'pseudowireprovider', 'networkControllerUrl')

class VnodLocalPseudowireConnectorServiceAdmin(XOSBaseAdmin):
    verbose_name = "VNOD Local Pseudowire Connector Service"
    verbose_name_plural = "VNOD Local Pseudowire Connector Service"
    list_display = ('servicehandle', 'internalport', 'pseudowirehandle','vnodlocal', 'administrativeState', 'operstate')
    list_display_links = ('servicehandle', 'internalport', 'pseudowirehandle','vnodlocal', 'administrativeState', 'operstate')

    fields = ('servicehandle', 'internalport', 'pseudowirehandle','vnodlocal', 'administrativeState', 'operstate')
    readonly_fields = ('vnodlocal', 'operstate', 'pseudowirehandle')


admin.site.register(VnodLocalSystem, VnodLocalSystemAdmin)
admin.site.register(VnodLocalService, VnodLocalServiceAdmin)
admin.site.register(VnodLocalPseudowireConnectorService, VnodLocalPseudowireConnectorServiceAdmin)


