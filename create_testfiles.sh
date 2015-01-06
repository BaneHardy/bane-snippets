#!/bin/sh

dd if=/dev/urandom bs=1MB of=015MB count=15
dd if=/dev/urandom bs=1MB of=020MB count=20
dd if=/dev/urandom bs=1MB of=050MB count=50
dd if=/dev/urandom bs=1MB of=100MB count=100
dd if=/dev/urandom bs=1MB of=150MB count=150
dd if=/dev/urandom bs=1MB of=200MB count=200
dd if=/dev/urandom bs=1MB of=250MB count=250
dd if=/dev/urandom bs=1MB of=500MB count=500
