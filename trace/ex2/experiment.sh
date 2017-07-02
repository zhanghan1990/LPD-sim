#!/bin/bash
## This is the DCTCP simulation result
./DCTCP.sh /root/project  100
./pfabric.sh /root/project 100
./D2TCP.sh /root/project  100
./LPD.sh /root/project  100
./timely.sh /root/project 100
