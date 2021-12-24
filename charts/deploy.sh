#!/usr/bin/env bash

source env.sh

imagedev=${DOCKER_ROOT}/${DEVBASE}${image}:${tag}
imagestag=${DOCKER_ROOT}/devops/stag/${image}:${tag}
imageprod=${DOCKER_ROOT}/devops/prod/${image}:${tag}

function mainmenu {
    clear
    echo
    echo -e "\t\t選單\n"
    echo -e "1. 更新程式"
    echo -e "2. build docker image"
    echo -e "3. 部署到Kubernetes"
    echo -e "0. 離開選單"
    #echo -en "\t\t請輸入選項(預設:2):"
    read -ep "請輸入選項(預設 0):" mainoption
    mainoption=${mainoption:-0}

}

function getCode {
    if ssh -A ${HOST} "[ -d ${TARGETROOT} ]"
    then
        echo "遠端目錄存在"
        ssh -A ${HOST} "mkdir -p ${APPROOT} && cd ${TARGETROOT} && git clean -n && git reset --hard && git pull origin -t '${tag}' "
    else
        echo "遠端目錄不存在"
        ssh -A ${HOST} "mkdir -p ${APPROOT} && cd ${APPROOT} && git clone -b '${tag}' ${GITROOT}${GIT_PROJ} ${PROJROOT}"
    fi
}

function pause {
    echo "任意鍵繼續"
    read -n 1
}

function show_info {
    echo "正式及測試環境需要你有足夠的權限才能正常執行"
    echo "開發環境image:${imagedev}"
    echo "測試環境image:${imagestag}"
    echo "正式環境image:${imageprod}"
}

function docker_build {
    while [[ true ]]
    do
        clear
        show_info
        echo
        echo -e "\t\t建制選單\n"
        echo -e "1. 開發環境(develop)"
        echo -e "2. 測試環境(staging)"
        echo -e "3. 正式環境"
        echo -e "0. 離開選單"
        read -ep "請輸入選項(預設 0):" option
        option=${option:-0}
        case ${option} in
            0)
                break
                ;;
            1)
                echo "開發環境"
                getCode
                echo "build image"
                ssh -A ${HOST} "cd ${TARGETROOT} && docker build -t ${imagedev} . --no-cache && docker login ${DOCKER_ROOT} && docker push ${imagedev}"
                pause
                break
                ;;
            2)
                echo "測試環境"
                ssh -A ${HOST} "docker login ${DOCKER_ROOT} && docker pull ${imagedev} && docker tag ${imagedev} ${imagestag} && docker push ${imagestag}"
                pause
                break
                ;;
            3)
                echo "正式環境"
                ssh -A ${HOST} "docker login ${DOCKER_ROOT} && docker pull ${imagestag} && docker tag ${imagestag} ${imageprod} && docker push ${imageprod}"
                pause
                break
                ;;
            *)
                clear
                echo "輸入的選項未知"
                ;;
        esac
        pause
    done
}

function k8s_stag {
    while [[ true ]]
    do
        clear
        echo
        echo -e "\t\tstaging環境選單\n"
        echo -e "1. create service"
        echo -e "2. delete service"
        echo -e "3. create ingress"
        echo -e "4. delete ingress"
        echo -e "0. 離開"
        read -ep "請輸入選項(預設 0):" option
        option=${option:-0}
        case ${option} in
            0)
                break
                ;;
            1)
                echo "create service"
                ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh apply svc stag"
                pause
                break
                ;;
            2)
                echo "delete service"
                ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh delete svc stag"
                pause
                break
                ;;
            3)
                echo "create ingress"
                ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh apply ing stag"
                pause
                break
                ;;
            4)
                echo "delete ingress"
                ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh delete ing stag"
                pause
                break
                ;;
            *)
                clear
                echo "輸入的選項未知"
                pause
                ;;
        esac
#        pause
    done
}

function k8s_prod {
    while [[ true ]]
    do
        clear
        echo
        echo -e "\t\tProduction環境選單\n"
        echo -e "1. create service"
        echo -e "2. delete service"
        echo -e "3. create ingress"
        echo -e "4. delete ingress"
        echo -e "0. 離開"
        read -ep "請輸入選項(預設 0):" option
        option=${option:-0}
        case ${option} in
            0)
                break
                ;;
            1)
                echo "create service"
                ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh apply svc prod"
                pause
                break
                ;;
            2)
                echo "delete service"
                ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh delete svc prod"
                pause
                break
                ;;
            3)
                echo "create ingress"
                ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh apply ing prod"
                pause
                break
                ;;
            4)
                echo "delete ingress"
                ssh -A ${HOST} "cd ${TARGETROOT}/charts && ./k8s_script.sh delete ing prod"
                pause
                break
                ;;
            *)
                clear
                echo "輸入的選項未知"
                ;;
        esac
        pause
    done
}

function createk8s {
    while [[ true ]]
    do
        clear
        echo
        echo -e "\t\tKubernetes選單\n"
        echo -e "1. 測試環境(staging)"
        echo -e "2. 正式環境"
        echo -e "0. 離開選單"
        read -ep "請輸入選項(預設 0):" option
        option=${option:-0}
        case ${option} in
            0)
                break
                ;;
            1)
                k8s_stag
                ;;
            2)
                k8s_prod
                ;;
            *)
                clear
                echo "輸入的選項未知"
                pause
                ;;
        esac
    done
}

while [[ 1 ]]
do
    mainmenu
    case ${mainoption} in
        0)
        break ;;
        1)
        echo "更新程式"
        getCode
        ;;
        2)
        echo "build docker images"
        docker_build
        ;;
        3)
        echo "部署到kubernetes"
        createk8s
        ;;
        *)
        clear
        echo "輸入的選項未知"
        pause
        ;;
    esac
done