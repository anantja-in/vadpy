#!/bin/bash

vadpy=$1/vad.py

function ftest_aurora_default {
    $vadpy ! aurora 
}

function ftest_run_param_h {
    $vadpy -h
}

function ftest_run_param_q {
    $vadpy -q
}

function ftest_run_noparam {
    $vadpy
}



function ftest 
{
    # echo functional test's name and call it
    # $1 function name
    # $2 expected exit status
    echo $1
    $1  # call vadpy

    exit_status=$?    
    exit_status_arg=0
    if [ $2 ] 
    then
        exit_status_arg=$2
    fi

    if [ $exit_status -ne $exit_status_arg ] 
    then
        echo $1 >> error.log  # log test name
    fi
}

ftest "ftest_run_noparam"
ftest "ftest_run_param_q" 
ftest "ftest_run_param_h"
ftest "ftest_aurora_default" 1