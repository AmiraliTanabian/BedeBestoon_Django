#!/bin/bash
source ./config.sh

curl -d "token=$token" $SITE_DOMAIN/api/general-stat
