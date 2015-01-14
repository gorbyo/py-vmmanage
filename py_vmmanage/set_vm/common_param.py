__author__ = 'Oleh Horbachov'


import argparse
import ConfigParser
import os
from argparse import RawTextHelpFormatter


def argument(cfgfile='config.ini'):

    if os.path.isfile(cfgfile):
        config = ConfigParser.RawConfigParser()
        config.read(cfgfile)

        parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                         description="This script clone new virtual machine on VMware host from exist "
                                                     "VM as template and create system in Cobbler for automatically "
                                                     "install.\n \n"
                                                     "For use this script need prepare Cobbler server with calling "
                                                     "profile like 'OS-TYPE' "
                                                     "(for example Centos7-WEB).\n \n"
                                                     "Usage with config file: \n"
                                                     "\t python %(prog)s \n"
                                        )

        parser.add_argument('-vmn', '--vmname', default=config.get('VM', 'name'),
                            help='This will be VM name for deploy')
        parser.add_argument('-vmos', '--vmosversion', default=config.get('VM', 'osversion'),
                            help='This will be VM OS for deploy')
        parser.add_argument('-vmt', '--vmtype', default=config.get('VM', 'type'),
                            help='This will be VM Type for deploy')
        parser.add_argument('-vme', '--vmenvironment', default=config.get('VM', 'environment'),
                            help='This will be environment for VM (available TEST, DEV, PROD)')
        parser.add_argument('-vmd', '--vmdatastore', default=config.get('VM', 'datastore'),
                            help='This will be environment for VM (available LUN(1,2,3,4)')

        parser.add_argument('-vH', '--vhost', default=config.get('VMWare', 'host'),
                            help='This will be hostname or ip address for VCenter')
        parser.add_argument('-vU', '--vusername', default=config.get('VMWare', 'username'),
                            help='This will be username for connect to VCenter')
        parser.add_argument('-vP', '--vpassword', default=config.get('VMWare', 'password'),
                            help='This will be password for connect to VCenter')

        parser.add_argument('-cH', '--chost', default=config.get('Cobbler', 'host'),
                            help='This will be hostname or ip address for Cobbler')
        parser.add_argument('-cU', '--cusername', default=config.get('Cobbler', 'username'),
                            help='This will be username for connect to Cobbler')
        parser.add_argument('-cP', '--cpassword', default=config.get('Cobbler', 'password'),
                            help='This will be password for connect to Cobbler')

    else:
        parser = argparse.ArgumentParser(description="Create VM in VCenter and Create Template in Cobbler %(prog)s")
        parser.add_argument('-vmn', '--vmname', default='TEST',
                            help='This will be VM name for deploy')
        parser.add_argument('-vmos', '--vmosversion', default='C7',
                            help='This will be VM OS for deploy')
        parser.add_argument('-vmt', '--vmtype', default='pure',
                            help='This will be VM Type for deploy')
        parser.add_argument('-vme', '--vmenvironment', default='PROD',
                            help='This will be environment for VM (available TEST, DEV, PROD)')
        parser.add_argument('-vmd', '--vmdatastore', default='LUN1',
                            help='This will be environment for VM (available LUN(1,2,3,4)')

        parser.add_argument('-vH', '--vhost', default='',
                            help='This will be hostname or ip address for VCenter')
        parser.add_argument('-vU', '--vusername', default='',
                            help='This will be username for connect to VCenter')
        parser.add_argument('-vP', '--vpassword', default='',
                            help='This will be password for connect to VCenter')

        parser.add_argument('-cH', '--chost', default='',
                            help='This will be hostname or ip address for Cobbler')
        parser.add_argument('-cU', '--cusername', default='',
                            help='This will be username for connect to Cobbler')
        parser.add_argument('-cP', '--cpassword', default='',
                            help='This will be password for connect to Cobbler')

    return parser.parse_args()

if __name__ == '__main__':
    cfg = 'config.ini'
    print (argument(cfg))
