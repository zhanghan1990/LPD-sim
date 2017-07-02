#!/bin/bash
## This is the DCTCP simulation result
./DCTCP.sh /home/zhanghan/pfabric-mahanmod/project 
./pfabric.sh /home/zhanghan/pfabric-mahanmod/project
./D2TCP.sh /home/zhanghan/pfabric-mahanmod/project
./LPD.sh /home/zhanghan/pfabric-mahanmod/project
./timely.sh /home/zhanghan/pfabric-mahanmod/project
