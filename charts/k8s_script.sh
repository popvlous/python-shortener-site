#!/usr/bin/env bash
if [[ ${1} != "apply" && ${1} != "delete" ]]
then
    echo "請輸入要建立(apply)或是刪除(delete)"
    exit
fi

if [[ ${2} != "svc" && ${2} != "ing"  ]]
then
    echo "請輸入建立service(svc)或是ingress(ing)"
    exit
fi

if [[ ${3} != "prod" && ${3} != "stag" ]]
then
    echo "請輸入測試(stag)或是正式(prod)環境"
    exit
fi

source env.sh

#if [[ $ ]]

#cat ./template/${2}-${3}.yaml
cat ./template/${2}-${3}.yaml | envsubst | kubectl ${1} -f -

