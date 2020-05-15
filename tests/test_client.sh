#!/bin/bash

echo
echo "************** START: test_client.sh **********************"

# Create temporary testing directory
echo "Creating temporary directory to work in."
here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

. $here/helpers.sh

# Make sure it's installed
if which qme >/dev/null; then
    printf "qme is installed\n"
else
    printf "qme is not installed\n"
    exit 1
fi

# Create temporary testing directory
tmpdir=$(mktemp -d)
output=$(mktemp ${tmpdir:-/tmp}/qme_test.XXXXXX)
config=$tmpdir/.qme
mkdir -p $config
printf "Created temporary directory to work in. ${output}\n"

echo
echo "#### Testing qme run"
runTest 0 $output qme --config_dir $config run ls

echo
echo "#### Testing qme get"
runTest 0 $output qme --config_dir $config get

echo
echo "#### Testing qme list"
runTest 0 $output qme --config_dir $config ls
runTest 0 $output qme --config_dir $config ls shell

echo 
echo "#### Testing qme clear"
runTest 0 $output qme --config_dir $config clear --force

rm -rf ${tmpdir}
