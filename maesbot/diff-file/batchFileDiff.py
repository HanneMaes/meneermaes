import os
import hashlib
import argparse # provides a convenient way to write user-friendly command-line interfaces

########################################################################################################################################################
# Get command line arguments

parser = argparse.ArgumentParser(description="Handle a command line variable") # creates an ArgumentParser object. The description parameter provides a brief explanation of what the script does, which will be displayed if the user runs the script with a -h or --help flag.
parser.add_argument("variable", help="The variable to be processed") # adds an argument to the parser. In this case, it's a positional argument named "variable". The help parameter provides a description of this argument, which will be shown in the help message.

args = parser.parse_args() # parses the command-line arguments
diffDir = args.variable

# print diff folder location
# print()
# print(f"Diffing all files in: {diffDir }")

########################################################################################################################################################
# Start the diff

namesAndHashes = []

# Get all files in the current dir and all subdirs, that are not hidden
for dirpath, dirnames, filenames in os.walk(diffDir):
    for dirname in dirnames:
        if dirname.startswith("."):
            dirnames.remove(dirname)
    for filename in filenames:
        if not filename.startswith(".") and filename != os.path.basename(__file__):

            # Exclude the script files
            if filename != "batchImageDiff.py" and filename != "LICENSE" and filename != "README.md":

                # Found a file that is not hidden in a dir that's not hidden
                filePath = os.path.join(dirpath, filename)

                # Hash the file
                h = hashlib.sha256() # make a hash object
                with open(filePath,'rb') as file: # open file for reading in binary mode
                    chunk = 0
                    while chunk != b'': # loop till the end of the file
                        chunk = file.read(1024) # read only 1024 bytes at a time
                        h.update(chunk)
                hashedFile = h.hexdigest() # return the hex representation of digest

                # Add to array
                namesAndHashes.append([filePath, hashedFile])

# Print all files
print()
print('Checking these ' + str(len(namesAndHashes)) + ' files:')
for i in namesAndHashes:
    print('   ➡️ ' + i[0])
    #print('   -> ' + i[0])
print()

# Sort array
namesAndHashes.sort(key=lambda namesAndHashes:namesAndHashes[1])

# Compare hashes
prevIsDifferent = False # True means that the prev loop iteration found a double
for i in range(0, len(namesAndHashes)-1): # len(namesAndHashes)-1 because I check with the next image, and the next image of the last image doesn't exist

    # Check if this file is the same as the next one
    if namesAndHashes[i][1] == namesAndHashes[i+1][1]:
        print('❌ ' + namesAndHashes[i][1] + ' ➡️ ' + namesAndHashes[i][0])
        #print('X ' + namesAndHashes[i][1] + ' ➡️ ' + namesAndHashes[i][0])
        prevIsDifferent = True
    else:
        # If the prev file was flagged as the same we always need a ❌, but we also need to check againt the next file
        if prevIsDifferent == False:
            print('🟢 ' + namesAndHashes[i][1])
            #print('V ' + namesAndHashes[i][1])
        else:
            print('❌ ' + namesAndHashes[i][1] + ' ➡️ ' + namesAndHashes[i][0])
            print('❌ ' + namesAndHashes[i][1] + ' ➡️ ' + namesAndHashes[i][0])
            #print('X ' + namesAndHashes[i][1] + ' ➡️ ' + namesAndHashes[i][0])
            #print('X ' + namesAndHashes[i][1] + ' ➡️ ' + namesAndHashes[i][0])
        prevIsDifferent = False

# Last image was already checked in the loop
lastItem = len(namesAndHashes) - 1
if prevIsDifferent == False: # If the prev file was flagged as the same we always need a ❌, but we also need to check againt the next file
    print('🟢 ' + namesAndHashes[lastItem][1])
    #print('V ' + namesAndHashes[lastItem][1])
else:
    print('❌ ' + namesAndHashes[lastItem][1] + ' ➡️ ' + namesAndHashes[lastItem][0])
    #print('X ' + namesAndHashes[lastItem][1] + ' ➡️ ' + namesAndHashes[lastItem][0])

print()
