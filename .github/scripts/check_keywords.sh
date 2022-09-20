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
keywords_string=$1
#keywords=("${@:2:$keywords_length}")

IFS=', ' read -r -a keywords <<< $keywords_string
keywords_length=${#keywords[@]}

changed_files=("${@:2}")
changed_files_length=${#changed_files[@]}
flag=false


# Check if first command-line arg exists as substring
# in any of the other command-line arg vars
for (( j=0; j<keywords_length; j++))
do
  for (( i=0; i<changed_files_length; i++ ));
  do
      if [[ "${changed_files[$i]}" = *"${keywords[$j]}"* ]]; then
          flag=true
          break
      fi
  done
done

echo $flag