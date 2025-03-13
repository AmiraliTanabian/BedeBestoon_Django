#!/bin/bash

source ./config.sh

curl -d "username=$1&password=$2" $SITE_DOMAIN/api/account/login