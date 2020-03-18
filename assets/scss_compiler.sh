#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCSS="${DIR}/scss/graphs.scss"
m1=$(md5sum "$SCSS")

while [ 1 ]
do
    sleep 2
    m2=$(md5sum "$SCSS")
    if [ "$m1" != "$m2" ] ; then
        echo "Detected change"
        OUTPUT="$(sass ${DIR}/scss/graphs.scss ${DIR}/css/graphs.css)"
        m1=$(md5sum "$SCSS")
        echo "${OUTPUT}"
    else
        echo "Detected no changes"
    fi
done
