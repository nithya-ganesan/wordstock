#!/bin/bash
# (C) Copyright 2019 Hewlett Packard Enterprise Development LP
set -eu -o pipefail
cd /
status=0
python /wordstock/tests/create_dataset.py \
    --datadir /data || status=$?

if [ $status -ne 0 ]; then
   exit 1
fi
