#!/bin/sh -l

echo "Start Install WHL Libiraries with parameters $1 $2 $3 $4 $5 "
time=$(date)
echo ::set-output name=time::$time

DBURL=$1
TOKEN=$2
CLUSTERID=$3
LIBS=$4
DBFSPATH=$5

echo "Install WHL Libiraries with parameters $DBURL $TOKEN $CLUSTERID $LIBS $DBFSPATH "

python3 ${SCRIPTPATH}/installWhlLibrary.py --workspace=${DBURL}\
                        --token=$TOKEN\
                        --clusterid=${CLUSTERID}\
                        --libs=$LIBS\
                        --dbfspath=${DBFSPATH}
