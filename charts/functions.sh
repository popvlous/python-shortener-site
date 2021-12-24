function getCode {
    if ssh -A ${HOST} "[ -d ${TARGETROOT} ]"
    then
        echo "遠端目錄存在"
        ssh -A ${HOST} "mkdir -p ${APPROOT} && cd ${TARGETROOT} && git clean -n && git reset --hard && git pull origin -t '${tag}' "
    else
        echo "遠端目錄不存在"
        ssh -A ${HOST} "mkdir -p ${APPROOT} && cd ${APPROOT} && git clone -b '${tag}' ${GITROOT}${GIT_PROJ} ${PROJROOT}"
    fi
#    pause
}

function pause {
    echo "任意鍵繼續"
    read -n 1
}