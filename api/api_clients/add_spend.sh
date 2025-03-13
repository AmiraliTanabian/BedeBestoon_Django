#!/bin/bash

source ./config.sh

curl -d "token=$token&price=$1&title=$2" $SITE_DOMAIN/api/submit/spend