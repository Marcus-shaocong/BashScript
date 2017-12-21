#!/bin/bash

set_bootctl(){
    SPIP=$1
    ssh root@$SPIP "boot_control.sh before c4-boot"
    echo "start to reboot $SPIP"
    ssh root@$SPIP "reboot -nf" 
}

install_sade(){
    SPIP=$1
    work_space=$2
    for saderpms in $( find $work_space/output/sade -name "dart*.rpm" )
    do
        echo "COMMAND: scp $saderpms root@$SPA:~"
        scp $saderpms root@$SPIP:~
        echo "COMMAND scp $saderpms root@$SPB:~"
        filename=`basename $saderpms`
        if [[ $filename =~ "safe-text" ]]
        then
            echo "skip safe-text"
        else
            echo "COMMAND: ssh root@$SPA rpm -Uvh $filename --nodeps --force"
            ssh root@$SPIP "rpm -Uvh $filename --nodeps --force"
        fi 
    done
}

install_safe(){
    SPIP=$1
    work_space=$2
    for saferpms in $( find $work_space/output/safe -name "safe*.rpm" )
    do
        echo "COMMAND: scp $saferpms root@$SPIP:~"
        scp $saferpms root@$SPIP:~
        filename=`basename $saferpms`
        if [[ $filename =~ "safe-text" ]]
        then
            echo "skip safe-text"
        else
            echo "COMMAND: ssh root@$SPIP rpm -Uvh $filename --nodeps --force"
            ssh root@$SPIP "rpm -Uvh $filename --nodeps --force"
        fi 
    done
}

WS="/home/c4dev/newphase"
SPA="10.245.101.120"
SPB="10.245.101.121"
is_dual_sp=false
SYSNAME=$1
if [[ -z $SYSNAME ]]
then
    SYSNAME="OB-H1160"
    echo $SYSNAME
fi
IncludeSade=$2
SPAOUT=`swarm $SYSNAME | grep "Lab IP SPA" | cut -d' ' -f6`
echo $SPAOUT
SPBOUT=`swarm $SYSNAME | grep "Lab IP SPB" | cut -d' ' -f6`
SPA=`echo $SPAOUT | cut -d' ' -f1`
echo "SPA: $SPA"
SPB=`echo $SPBOUT | cut -d' ' -f2`
echo "SPB: $SPB"

if [[ $SPB == "" ]]
then
    echo "SPB IP is empty, It's single SP"
else
    echo "It's dual SP"
    is_dual_sp=true
fi


set_bootctl $SPA & 
if [ $is_dual_sp = true ]
then
    set_bootctl $SPB &
fi

wait

sleep 10
while true
do
    echo "start ping spa..."
    ping -w 4 $SPA
    if [[ $? -eq 0 ]] 
    then
        break
    fi
done

if [ $is_dual_sp = true ]
then
    while true
    do
        echo "start ping spa..."
        ping -w 4 $SPB
        if [[ $? -eq 0 ]] 
        then
            break
        fi
    done
fi

install_sade $SPA $WS &
install_safe $SPA $WS &
if [ $is_dual_sp = true ]
then
    install_sade $SPB $WS &
    install_safe $SPB $WS &
fi
wait

ssh root@$SPA "boot_control.sh before c4-boot clear"
ssh root@$SPA "boot_control.sh continue"
ssh root@$SPA "rm -rf *.rpm"

if [ $is_dual_sp = true ]
then
    ssh root@$SPB "boot_control.sh before c4-boot clear"
    ssh root@$SPB "boot_control.sh continue"
    ssh root@$SPB "rm -rf *.rpm"
fi

echo "finished"


