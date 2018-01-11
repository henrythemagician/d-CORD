
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


# Dockerfile for onos-apps maven repo

FROM maven:3-jdk-8 as maven
COPY settings.xml /root/.m2/settings.xml
COPY . /mavenwd
WORKDIR /mavenwd/apps
RUN mvn dependency:copy-dependencies -Dmdep.copyPom=false -Dmdep.useRepositoryLayout=true -DoutputDirectory=m2/repository -Dmdep.addParentPoms=false -Dtype=oar -DexcludeTypes=jar -Dsilent=true -f dependencies.xml

FROM nginx
WORKDIR /usr/share/nginx/html
COPY --from=maven /mavenwd/repository repository
RUN chown nginx:nginx -R /usr/share/nginx/html/repository

# Label image
ARG org_label_schema_schema_version=1.0
ARG org_label_schema_name=opencord/mavenrepo
ARG org_label_schema_version=unknown
ARG org_label_schema_vcs_url=unknown
ARG org_label_schema_vcs_ref=unknown
ARG org_label_schema_build_date=unknown
ARG org_opencord_vcs_commit_date=unknown

LABEL org.label-schema.schema-version=$org_label_schema_schema_version \
      org.label-schema.name=$org_label_schema_name \
      org.label-schema.version=$org_label_schema_version \
      org.label-schema.vcs-url=$org_label_schema_vcs_url \
      org.label-schema.vcs-ref=$org_label_schema_vcs_ref \
      org.label-schema.build-date=$org_label_schema_build_date \
      org.opencord.vcs-commit-date=$org_opencord_vcs_commit_date
