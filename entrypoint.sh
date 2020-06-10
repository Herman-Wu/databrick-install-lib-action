#!/bin/sh -l

echo "Hello $1 $2 $3 $4 $5 "
time=$(date)
echo ::set-output name=time::$time

DBURL=$1
TOKEN=$2
CLUSTERID=$3
LIBS=$4
DBFSPATH=$5


echo "Hello2 $DBURL $TOKEN $CLUSTERID $LIBS $DBFSPATH "

python3 ${SCRIPTPATH}/installWhlLibrary.py --workspace=${DBURL}\
                        --token=$TOKEN\
                        --clusterid=${CLUSTERID}\
                        --libs=$LIBS\
                        --dbfspath=${DBFSPATH}

echo "Install Libraries Done"