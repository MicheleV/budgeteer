#!/bin/sh
#
# Start a Centos8 VM and reboot it

# Get CentOS Minimal from http://isoredirect.centos.org/centos/7/isos/x86_64/
# /var/lib/libvirt/images/CentOS-7-x86_64-Minimal-1908.iso should be owned by qemu:qemu

# root user, password "root" user "cloud-user", password "123456" as per kickstart.cfg
vm_name=centos8-vm
iso_path=/var/lib/libvirt/images/CentOS-Stream-x86_64-dvd1.iso
ks_path=./centos8.cfg
disk_path=/var/lib/libvirt/images/centos8.qcow2
network_name=default

# NOTE --wait=-1 make sure the reboot is issued after installation is complete
# as per https://access.redhat.com/solutions/41976

# virt-install --name $vm_name \
# --cdrom $iso_path \
# --initrd-inject centos8.cfg \
# --memory=2048 --vcpus=2 --disk size=10 \
# --extra-args "ks=file:/centos8.cfg console=ttyS0,115200" \
# --noautoconsole --wait=-1 --serial pty --console pty

virt-install \
    --name $vm_name \
    --initrd-inject $ks_path \
    --virt-type kvm \
    --ram 2048 \
    --vcpus 2 \
    --arch x86_64 \
    --cpu kvm64 \
    --os-type linux \
    --os-variant centos7.0 \
    --disk path=$disk_path,format=qcow2,bus=virtio,cache=none \
    --location $iso_path \
    --serial pty \
    --extra-args "edd=off console=tty0 console=ttyS0,115200 ks=file:/centos8.cfg" \
    --noautoconsole \
    --wait=-1

vm_ip=$(virsh net-dhcp-leases $network_name | grep $(virsh dumpxml $vm_name | grep "mac address" | awk -F\' '{ print $2}' ) | awk '{print $5}')
echo "VM $vm_name IP is: $vm_ip"