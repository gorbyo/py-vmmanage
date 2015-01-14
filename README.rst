py_vmmanage
=====

This script clone new virtual machine on VMware host from exist VM as template and create system in Cobbler
for automatically install.
Create VM in VCenter and Create Template in Cobbler.
For use this script need prepare Cobbler server with calling profile like 'OS-TYPE' (for example Centos7-WEB).

    Usage with config file:
        python py-vmware.py

    Usage without config file:
        python py-vmware.py --chost='cobbler_host_or_ip' --cusername='cobbler_username' --cpassword='cobbler_password' --vhost='vcenter_host_or_ip' --vusername='vcenter_username' --vpassword='vcenter_password' --vmdatastore='datastore' --vmenvironment='pool' --vmname='vm_name' --vmosversion='Centos7' --vmtype='WEB'
