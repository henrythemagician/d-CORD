# Building a Local ONOS Docker Image with Control Plane Applications

Included in this area is a `Dockerfile` that can be use to build a Docker
image of the ONOS application with the local build of the control plane
applications required to run VOLTHA. This file can be found in
`<ROOT>/onos-apps/docker/Dockerfile.onos`. To build the image use the following
commands:

```
$ cd <ROOT>/onos-apps
$ docker build -f  docker/Dockerfile.onos -t onos:local .
```

This will create a Docker image named (tagged) `onos:local`. To run invoke
an instance of this container the following command can be used:

```
$ docker run -ti onos:local
```

This will invoke the container instance in the foreground, which is not
something that would typically be done in production, but works for a
simple verification.

Once ONOS is started and initialized the command `apps -s -a` should present
the following installed and activated applications:

```
onos> apps -s -a
*   5 org.onosproject.drivers              1.8.5.SNAPSHOT Default device drivers
*   6 org.onosproject.optical-model        1.8.5.SNAPSHOT Optical information model
*  25 org.onosproject.netcfghostprovider   1.8.5.SNAPSHOT Network Config Host Provider
*  40 org.onosproject.ovsdb-base           1.8.5.SNAPSHOT OVSDB Provider
*  41 org.onosproject.drivers.ovsdb        1.8.5.SNAPSHOT OVSDB Device Drivers
*  69 org.onosproject.openflow-base        1.8.5.SNAPSHOT OpenFlow Provider
*  85 org.onosproject.netcfglinksprovider  1.8.5.SNAPSHOT Network Config Link Provider
*  86 org.opencord.config                  1.2.0.SNAPSHOT CORD configuration meta application
*  87 org.opencord.vtn                     1.2.0.SNAPSHOT VTN App
*  89 org.opencord.dhcpl2relay             1.0.0.SNAPSHOT DHCP Relay Agent App
*  90 org.opencord.mcast                   1.2.0.SNAPSHOT CORD Multicast application
*  91 org.opencord.sadis                   1.0.0.SNAPSHOT Subscriber And Device Information App
*  92 org.opencord.igmpproxy               1.0.0.SNAPSHOT IGMP PROXY APP
*  93 org.onosproject.olt                  1.2.0.SNAPSHOT Optical Line Terminal App
*  94 org.opencord.aaa                     1.2.0.SNAPSHOT AAA App
*  95 org.opencord.igmp                    1.2.0.SNAPSHOT Internet Group Message Protocol
```

*NOTE: If the command `apps -s -a` is issued before `ONOS` is complete
initialized errors will be reported to the console. It can take seconds to
minutes for ONOS to be initialized.*
