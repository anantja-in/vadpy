#!/bin/bash

vadpy=$1/vad.py


function ftest_nist08_default {
    $vadpy ! nist08
}

function ftest_nist05_default {
    $vadpy ! nist05
}


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

function ftest_nist08
{
    ftest "ftest_nist08_default"
}

function ftest_nist05
{
    ftest "ftest_nist05_default"
}

function ftest_aurora 
{
    ftest "ftest_aurora_default"
}

ftest "ftest_run_noparam"
ftest "ftest_run_param_q" 
ftest "ftest_run_param_h"
ftest "ftest_aurora"
ftest "ftest_nist08"
ftest "ftest_nist05"