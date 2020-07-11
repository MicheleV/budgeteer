#!/bin/sh
#
# Start a Centos8 VM and reboot it

# Get CentOS Minimal from http://isoredirect.centos.org/centos/7/isos/x86_64/
# /var/lib/libvirt/images/CentOS-7-x86_64-Minimal-1908.iso should be owned by qemu:qemu

# root user, password "root" user "cloud-user", password "123456" as per centos8.cfg
vm_name=centos8-vm
#CentOS-Stream-8-x86_64-20200629-dvd1.iso
iso_path=/var/lib/libvirt/images/CentOS-Stream-x86_64-dvd1.iso
ks_path=./centos8.cfg
disk_path=/var/lib/libvirt/images/centos8.qcow2
network_name=default


qemu-img create -f qcow2 centos8.qcow2 6G
mv centos8.qcow2 /var/lib/libvirt/images/centos8.qcow2
chown qemu:qemu /var/lib/libvirt/images/centos8.qcow2
# restorecon -rvvf /var/lib/libvirt/images/

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
# NOTE --wait=-1 make sure the reboot is issued after installation is complete
# as per https://access.redhat.com/solutions/41976

vm_ip=$(virsh net-dhcp-leases $network_name | grep $(virsh dumpxml $vm_name | grep "mac address" | awk -F\' '{ print $2}' ) | awk '{print $5}')
echo "VM $vm_name IP is: $vm_ip"