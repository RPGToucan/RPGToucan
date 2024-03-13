def lcf_to_dict(path):
    loadedFile = []
    exportedDict = {}
    # Open the file.
    with open(path, 'rb') as file:
        while True:
            read = file.read(1)
            if not read:
                break
            loadedFile.append(read.hex())


    # Get header. Headers lack ids, so we separate it to prevent errors.
    header = ""
    length = int(loadedFile[0], 16)
    for currentByte in range(1, length + 1):
        header += chr(int(loadedFile[currentByte], 16))
    currentByte += 1

    # Loading hardcoded data starts here.
    # Use header to get id list.
    if header == "LcfMapTree":
        from pylcf.filetypes import LcfMapTree as lcfInfo
    elif header == "LcfDatabase":
        from pylcf.filetypes import LcfDatabase as lcfInfo
    elif header == "LcfMapUnit":
        from pylcf.filetypes import LcfMapUnit as lcfInfo
    else: print("The file lacks a valid header!")
    storeType = lcfInfo.storeType
    typesDict = lcfInfo.typesDict
    # Event array layout. The event array is a dictionary.
    # The meta events count is excluded, as it is handled externally.

    # End of hardcoded data.

    exportedDict = {}
    length = 0

    # Converting the file to a dictionary begins here.
    while not currentByte > len(loadedFile):
        if length == 0:
            exportedItem = None
            current_id = int(loadedFile[currentByte],16)
            currentByte +=1
            try: typesDict[current_id]["type"]
            except KeyError:
                print("Cannot find key"+str(current_id))
                break
            print("Reading key", current_id)
            # Get length. The length is a regular int.
            leftmostByte = 1
            lengthCalcB = ''
            while int(leftmostByte) != 0:
                # if i put the [1:], [:1] etc. right after the format, it just doesn't work. python bug, probably
                lengthCalc = format(int(loadedFile[currentByte], 16), '08b')
                lengthCalc = lengthCalc[1:]
                lengthCalcB += lengthCalc
                leftmostByte = format(int(loadedFile[currentByte], 16), '08b')
                leftmostByte = leftmostByte[:1]
                currentByte += 1
            currentByte -= 1
            length = int(lengthCalcB, 2)
            # i'd assume that putting the while inside there is faster
            # Convert the content.
            intCalcB = ''
            while length > 0:
                currentByte += 1
                if typesDict[current_id]["type"] == "str":
                    try: exportedItem += chr(int(loadedFile[currentByte], 16))
                    except TypeError: exportedItem = chr(int(loadedFile[currentByte], 16))
                elif typesDict[current_id]["type"] == "bool":
                    exportedItem = bool(loadedFile[currentByte])
                elif typesDict[current_id]["type"] == "int":
                    # welcome to the int zone. how tough are ya
                    leftmostByte = format(int(loadedFile[currentByte], 16), "b")[:1]
                    # if i put the [1:], [:1] etc. right after the format, it just doesn't work. python bug, probably
                    intCalc = format(int(loadedFile[currentByte], 16), '08b')
                    intCalc = intCalc[1:]
                    intCalcB += intCalc
                    if intCalcB == '':
                        exportedItem = 0
                        # python truncates empty binary to an empty string for some reason
                    else: exportedItem = int(intCalcB, 2)
                elif typesDict[current_id]['type'] == "binary":
                    # used for stuff like map contents afaik. convertible to normal uints apparently
                    # just a note: in map terms each tile is 2 bytes, the formula for map length is width x height x 2
                    try: exportedItem.append(loadedFile[currentByte])
                    except AttributeError: exportedItem = [loadedFile[currentByte]]
                elif typesDict[current_id]['type'] == "event_array":
                    # yeah i'll just dummy this out for now.
                    try: exportedItem.append(loadedFile[currentByte])
                    except AttributeError: exportedItem = [loadedFile[currentByte]]

                length -= 1
            currentByte += 1
        exportedDict[current_id] = exportedItem
    dictName = exportedDict

    # If any keys are missing due to being the default value, add them here.
    # They're removed when exporting back to a file anyway.
    for key in typesDict:
        if not exportedDict.__contains__(key) and not typesDict[key].__contains__("optional"):
            try: exportedDict[key] = typesDict[key]["default"]
            except KeyError: print("WARNING: No default for ID "+str(key))

    return dictName

def dict_to_lcf():
    print("bogus")

# example = lcf_to_dict(r"D:\games and tools\dev\Example Project\Map0001.lmu")
# dict_to_lcf()
# print(example)