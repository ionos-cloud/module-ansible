###
# This script checks if the first command-line argument exists
# as a substring in any of the next provided command-line arguments
# (by using globbing) - i.e. *foo* in foobar returns true
#
# For use with Github Actions
#
# Example: bash string_in_array.sh hi qwerty ahia ohio hello asdf
# output: ::set-output name=exists::true
#

# All command-line args except the first go into 'arr' variable 
arr=("${@:2}")
flag=false

# Check if first command-line arg exists as substring
# in any of the other command-line arg vars
for (( i=0; i<${#arr[@]}; i++ ));
do
    if [[ "${arr[$i]}" = *"${1}"* ]]; then
        flag=true
        break
    fi
done

echo $flag