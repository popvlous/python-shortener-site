#!/usr/bin/env bash

export tag="0.0.21"
export replicas=2
export PORTS=5005
# git專案目錄為
# https://gitlab.nexuera.com/ams/python-agora-backend.git
# 請填以下資訊
export PROJROOT="python-agora-backend"
export GIT_PROJ="ams/python-agora-backend.git"

# 自定義
export image="backend"
export svc="backend"
export namespace="agora"
export STAG_URL="agoraite.nexuera.com"
export STAG_TLS="cf-tls"
export PROD_URL="agora.pyrarc.com"
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


