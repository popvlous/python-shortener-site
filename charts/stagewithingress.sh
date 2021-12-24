#!/usr/bin/env bash

source env.sh
source functions.sh

imagedev=${DOCKER_ROOT}/${DEVBASE}${image}:${tag}
imagestag=${DOCKER_ROOT}/devops/stag/${image}:${tag}
#imageprod=${DOCKER_ROOT}/devops/prod/${image}:${tag}

getCode
echo "build image"
ssh -A ${HOST} "cd ${TARGETROOT} && docker build -t ${imagedev} . --no-cache && docker login ${DOCKER_ROOT} && docker push ${imagedev}"
echo "測試環境"
ssh -A ${HOST} "docker login ${DOCKER_ROOT} && docker pull ${imagedev} && docker tag ${imagedev} ${imagestag} && docker push ${imagestag}"
#echo "正式環境"
#ssh -A ${HOST} "docker login ${DOCKER_ROOT} && docker pull ${imagestag} && docker tag ${imagestag} ${imageprod} && docker push ${imageprod}"
#echo "delete service"
#ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh delete svc prod"
echo "create service"
ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh apply svc stag"
#echo "delete ingress"
#ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh delete ing stag"
echo "create ingress"
ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh apply ing stag"

