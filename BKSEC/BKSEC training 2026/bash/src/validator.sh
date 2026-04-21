#!/bin/bash
readonly ERR_INVALID="ERR_INVALID_REQUEST"
readonly ERR_TIMESTAMP="ERR_TIMESTAMP_LENGTH"
readonly ERR_NOTFOUND="ERR_FILE_NOT_FOUND"
readonly ERR_TIMEWINDOW="ERR_TIME_WINDOW_INVALID"
a=""
ki=""
tb=""
te=""
sg=""
fn=""
x=""
process_request() {
    local input="$1"
    local err=""
    IFS='_' read -ra parts <<< "$input"
    local params="${parts[0]}"
    IFS=',' read -ra pairs <<< "$params"
    for pair in "${pairs[@]}"; do
        k="${pair%%=*}"
        x="${pair##*=}"
        case ${k} in
            ki) ki="${x}" ;;
            tb) 
                tb="${x}"
                if (( ${#tb} != 10 )); then
                    err="${ERR_TIMESTAMP}"
                fi
                ;;
            te) 
                te="${x}"
                if (( ${#te} != 10 )); then
                    err="${ERR_TIMESTAMP}"
                fi
                ;;
            sg) sg="${x}" ;;
            *) err="${ERR_INVALID}" ;;
        esac
    done
    if [[ -n ${err} ]]; then
        echo "${err}"
        return 1
    fi
    now=$(date +%s)
    if [[ ${now} -gt ${tb} ]]; then
        if [[ ${now} -lt ${te} ]]; then
            fn="${parts[2]}"
            path="/opt/storage/files/uploads/public/${fn}"
            if [[ -f "${path}" ]]; then
                echo "${path}"
                return 0
            else
                echo "${ERR_NOTFOUND}"
                return 1
            fi
        else
            echo "${ERR_TIMEWINDOW}"
            return 1
        fi
    else
        echo "${ERR_TIMEWINDOW}"
        return 1
    fi
}
while read -r line; do
    result=$(process_request "$line")
    echo "$result"
done
