#!/bin/bash

echo "starting node in daemon mode..."
echo "running on testnet, call the daemon with: ~/Hydra/bin/./hydra-cli -testnet getinfo"

./hydrad -daemon -testnet -datadir=/usr/share/hydranode/datadir -staking=false

while true; do sleep 30; done;
