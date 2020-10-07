#!/bin/sh

#############################
### HOST SETUP (Fedora32) ###
#############################

## Download the image
#sudo dnf -y install coreos-installer fcct ignition-validate
#STREAM="stable"
#coreos-installer download -s "${STREAM}" -p qemu -f qcow2.xz --decompress -C ~/.local/share/libvirt/images/

## Rename it
#mv /home/<username>/.local/share/libvirt/images/fedora-coreos-*.qcow2 .
#mv fedora-coreos-*.qcow2 fedora-coreos.qcow2

## Move it in place, adjust permissions
#sudo cp /home/<username>/coreos/fedora-coreos.qcow2 /var/lib/libvirt/images/
#sudo chown qemu:qemu /var/lib/libvirt/images/fedora-coreos.qcow2 # restorecon is executed in the rebuild part

## Confirm libvirtd is running correctly
#sudo systemctl status -fl libvirtd

###################
### DANGER ZONE ###
###################

#sudo virsh destroy fcos
#sudo virsh undefine --remove-all-storage fcos

###############
### REBUILD ###
###############

fcct --pretty --strict budgeteer-fedoracoreos-ignition.yaml --output budgeteer-fedoracoreos-ignition.ign
ignition-validate budgeteer-fedoracoreos-ignition.ign && echo 'Success!' # TODO: add exit 1 and show an error message on failure
sudo cp budgeteer-fedoracoreos-ignition.ign /var/lib/libvirt/images/
sudo chown qemu:qemu -Rvv /var/lib/libvirt/images/
sudo restorecon -Rvv /var/lib/libvirt/images/

# TODO: --cpu host is needed in order to avoid errors thrown by qemu-kvm not recognizing "-fw_cfg" option
#      see if this is qemu-kvm version specific https://github.com/coreos/bugs/issues/1783

# TODO: use variables for cpu,ram, etc
sudo virt-install --name=fcos --vcpus=2 --cpu host --ram=2048 --os-variant=fedora32 \
    --import --network=bridge=virbr0 --graphics=none \
    --qemu-commandline="-fw_cfg name=opt/com.coreos/config,file=/var/lib/libvirt/images/budgeteer-fedoracoreos-ignition.ign" \
    --disk=size=20,backing_store=/var/lib/libvirt/images/fedora-coreos.qcow2