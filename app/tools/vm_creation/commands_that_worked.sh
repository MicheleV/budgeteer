sudo virt-install --name centos8-vm --arch x86_64 \
--os-variant centos7.0 --vcpus 4 --memory 4096 \
--network default --graphics vnc --noautoconsole \
--cdrom /var/lib/libvirt/images/CentOS-Stream-x86_64-dvd1.iso \
--disk /var/lib/libvirt/images/centos8.qcow2

sudo virt-install --name centos8-vm --arch x86_64 \
--os-variant centos7.0 --vcpus 4 --memory 4096 --network default  \
--noautoconsole --location /var/lib/libvirt/images/CentOS-Stream-x86_64-dvd1.iso \
--disk /var/lib/libvirt/images/centos8.qcow2 
