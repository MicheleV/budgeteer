#!/bin/sh
#
# Start a Centos VM and reboot it

# Get CentOS Minimal from http://isoredirect.centos.org/centos/7/isos/x86_64/
# /var/lib/libvirt/images/CentOS-7-x86_64-Minimal-1908.iso should be owned by qemu:qemu

# root user, password "root" user "cloud-user", password "123456" as per kickstart.cfg
vm_name=my-new-vm
iso_path=/var/lib/libvirt/images/CentOS-7-x86_64-Minimal.iso
network_name=default

# NOTE --wait=-1 make sure the reboot is issued after installation is complete
# as per https://access.redhat.com/solutions/41976

virt-install --name $vm_name \
--location $iso_path \
--initrd-inject kickstart.cfg \
--memory=1024 --vcpus=1 --disk size=10 \
--extra-args "ks=file:/kickstart.cfg console=ttyS0,115200" \
--noautoconsole --wait=-1 --serial pty --console pty


vm_ip=$(virsh net-dhcp-leases $network_name | grep $(virsh dumpxml $vm_name | grep "mac address" | awk -F\' '{ print $2}' ) | awk '{print $5}')
echo "VM $vm_name IP is: $vm_ip"