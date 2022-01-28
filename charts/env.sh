#!/usr/bin/env bash

export tag="0.0.17"
export replicas=2
export PORTS=5005
# git專案目錄為
# https://gitlab.nexuera.com/fred/python-ams-comsumer.git
# 請填以下資訊
export PROJROOT="python-ams-comsumer"
export GIT_PROJ="fred/python-ams-comsumer.git"

# 自定義
export image="comsumer"
export svc="comsumer"
export namespace="agora"
export STAG_URL="agoraweb.nexuera.com"
export STAG_TLS="cf-tls"
export PROD_URL="agoraweb.pyrarc.com"
export PROD_TLS="cf-tls"
# 假定所有的專案都放在~/apps底下
export APPROOT="~/apps"
export TARGETROOT=${APPROOT}/${PROJROOT}
export GITROOT="https://gitlab.nexuera.com/"
export DOCKER_ROOT="registry.nexuera.com"
export DEVBASE="devops/dev/"
export DEVSTAG="devops/stag"
export DEVPROD="devops/prod"

source hosts.sh


