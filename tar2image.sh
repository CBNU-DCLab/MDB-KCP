#!/bin/bash
newcontainer=$(buildah from scratch)
path=$1
buildah add $newcontainer $path /
buildah config --annotation=io.kubernetes.cri-o.annotations.checkpoint.name=redis-snpashot $newcontainer
buildah commit $newcontainer redis-snapshot:latest
buildah rm $newcontainer
