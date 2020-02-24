#!/bin/sh

# Get CentOS Minimal from http://isoredirect.centos.org/centos/7/isos/x86_64/
# The vm is created with user "cloud-user", password "123456"
sudo virt-install --name  \
--location ./CentOS-7-x86_64-Minimal.iso \
--initrd-inject ks.cfg \
--extra-args "ks=file:/ks.cfg console=ttyS0,115200" \
--memory=1024 --vcpus=1 --disk size=5 \
--noautoconsole --graphics vnc --serial pty --console pty

# TODO: try to add --nographic instead of vnc