#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  Copyright 2014 Oleh Horbachov <gorbyo@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


"""
This script clone new virtual machine on VMware host from exist VM as template and create system in Cobbler
for automatically install.
Create VM in VCenter and Create Template in Cobbler %(prog)s
For use this script need prepare Cobbler server with calling profile like 'OS-TYPE' (for example Centos7-WEB).

Usage with config file:
    python py-vmware.py

Usage without config file:
    python py-vmware.py --chost='cobbler_host_or_ip' --cusername='cobbler_username' --cpassword='cobbler_password' \
        --vhost='vcenter_host_or_ip' --vusername='vcenter_username' --vpassword='vcenter_password' \
        --vmdatastore='datastore' --vmenvironment='pool' --vmname='vm_name' --vmosversion='Centos7' --vmtype='WEB'
"""

__author__ = 'Oleh Horbachov'

import xmlrpclib
from pysphere import VIServer
from set_vm import vm_param, common_param

vm_templates = {'DEV': 'DEV_TEMPLATE', 'PROD': 'PROD_TEMPLATE'}


def virtual_conn():
    srv = VIServer()
    srv.connect(common_param.argument().vhost, common_param.argument().vusername, common_param.argument().vpassword)
    return srv


def list_vms(srv):
    vms = srv.get_registered_vms()
    for vm in vms:
        virtual_machine = srv.get_vm_by_path(vm)
        print virtual_machine.get_resource_pool_name(), '|', virtual_machine.get_property('name'), '|', \
            virtual_machine.get_property('ip_address'), '|', virtual_machine.get_status()


def create_vm(srv):
    if common_param.argument().vmenvironment == 'PROD':
        vm = srv.get_vm_by_name(vm_templates.get('PROD'))
    else:
        vm = srv.get_vm_by_name(vm_templates.get('DEV'))

    vm.clone(common_param.argument().vmenvironment+'_' + common_param.argument().vmname, power_on=False,
             resourcepool=vm_param.set_resource_pool(srv, common_param.argument().vmenvironment),
             datastore=vm_param.set_data_store(srv, common_param.argument().vmdatastore))
    return 0


def cobb_conn():
    srv = xmlrpclib.Server("http://"+common_param.argument().chost+"/cobbler_api")
    token = srv.login(common_param.argument().cusername, common_param.argument().cpassword)
    return srv, token


def get_mac_address(vm):
    mac_list = []
    net = vm.get_property('net', from_cache=False)
    if net:
        for interface in net:
            if interface.get('mac_address', None):
                mac_list.append(interface.get('mac_address', None))
    else:
        for v in vm.get_property('devices').values():
            if v.get('macAddress'):
                mac_list.append(v.get('macAddress'))

    return mac_list


def set_profile(srv, token, mac_address):
    system_id = srv.new_system(token)
    srv.modify_system(system_id, 'name', common_param.argument().vmenvironment + '_' + common_param.argument().vmname,
                      token)
    srv.modify_system(system_id, 'profile', common_param.argument().vmosversion + '-' + common_param.argument().vmtype,
                      token)
    srv.modify_system(system_id, 'modify_interface', {
        'macaddress-eth0': mac_address,
        }, token)
    srv.save_system(system_id, token)


def main():
    vserver = virtual_conn()
    create_vm(vserver)
    newvm = vserver.get_vm_by_name(common_param.argument().vmenvironment+'_' + common_param.argument().vmname)
    set_profile(token=cobb_conn()[1], srv=cobb_conn()[0], mac_address=get_mac_address(vm=newvm)[0])
    newvm.power_on(sync_run=False)
    vserver.disconnect()


if __name__ == '__main__':
    cfg = 'config.ini'
    print (common_param.argument())
    main()