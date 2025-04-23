from functions import *

FILE_CONVERTING = "input.asm"

file_data = getFileData(FILE_CONVERTING)

if file_data:
    parsed_data = parse(file_data)
    print("")
    print("Result:\n")
    print(parsed_data)
    print("")
