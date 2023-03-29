#!/bin/bash

/sbin/modinfo -F filename kvm > /dev/null 2>&1
if [ $? -eq 0 ]; then
    /sbin/modprobe virtio_console
    /sbin/modprobe virtio_blk
    /sbin/modprobe virtio_net
    /sbin/modprobe virtio_scsi
fi
