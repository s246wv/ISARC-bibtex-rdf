#!/bin/bash

ttl=${1/.ttl/}
query=$2

python embed.py ${ttl}.ttl ${query} ${ttl}.emb
python compare.py ${ttl}.emb.json ${ttl}_acm_ccs
python addSim2Ttl.py ${ttl}.ttl ${ttl}_acm_ccs_top5.json ${ttl}_2
mkdir export
mv ${ttl}* ./export
mv ./export/${ttl}_2.ttl ./${ttl}.ttl
