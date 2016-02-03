#!/bin/bash

# Script to replace the space in filenames with another char like '-' and copy 
# to a new folder.  All done the bash way.
# 02-03-2016 Prech Uapinyoying

# Example:
# '2016_02_01 04_36_28.06.fb.txtSensor1.txt' originals with space
# '2016_02_01 04_36_28.06.fb.txtSensor2.txt' 
# '...'
# '2016_02_01-04_36_28.06.fb.txtSensor1.txt' renamed with '-'
# '2016_02_01-04_36_28.06.fb.txtSensor2.txt' 

# Useful links
    # If you run into problems with spaces when dealing with 'for' loops
    #     https://bash.cyberciti.biz/guide/$IFS
    #     http://stackoverflow.com/questions/16831429/when-setting-ifs-to-split-on-newlines-why-is-it-necessary-to-include-a-backspac

    # If you want to do indexing over arrays
    #     http://stackoverflow.com/questions/6723426/looping-over-arrays-printing-both-index-and-value
    #     http://stackoverflow.com/questions/1878882/arrays-in-unix-shell
    #     http://stackoverflow.com/questions/1951506/bash-add-value-to-array-without-specifying-a-ke

# set the Internal Field Separator to new line, $ sign is important can also do IFS='\n\b'
# Without this specification, the for loop will separate spaces, tabs AND newlines
IFS=$'\n'

# Find and make a list of all files in the current directory, specific == good
# We want the original names and the renamed ones. Full paths can be handy

# We must add the '\' in front of the space so cp command will understand
# Change '*.txtSensor?.txt' to whatever is specific to your filenames
ORIG_FILENAMES=$(find $PWD -name '*.txtSensor?.txt' | sed 's/ /\ /')
# for file in $ORIG_FILENAMES; do
#    echo $file

# Use sed to replace space with '-' or any other non-white-space character
NEW_FILENAMES=$(find $PWD -name '*.txtSensor?.txt' | sed 's/ /-/')
# echo $NEW_FILENAMES

# Turn these lists into an shell arrays so we can use indexes 
# Values are separate by '\n' because of the IFS=$'\n' above, not spaces
orig_array=($ORIG_FILENAMES)

# For the new names, we will do something a little different. We just want the
# basename of the file so we can use it to copy to a separate directory
new_array=()
for path in $NEW_FILENAMES; do 
    new_array+=($(basename $path)) 
done
# echo ${new_array[@]}

# make a new directory to house the renamed files
mkdir renamed
cd renamed

# The ! in front of the array variable turns the 'i' into the array int key instead 
# of the array value
for i in "${!orig_array[@]}"; do
    $(cp "${orig_array[$i]}" ${new_array[$i]})
done

echo "Finished renaming the files. Find them in the './renamed/' directory"
