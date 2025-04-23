operators = {
    "global": "001",

    "mov": "016",
    "org": False,
    "int": "017",
    "ret": "018",
    "loop": "019",
    "add": "020",
    "xor": "021",
    "len": "022",
    "equ": "023",
    "$": "024",

    "+": "025",
    "-": "026",
    
    "stosb": "032",
    "stosw": "033",
    "stosd": "034",
    "msg": "035",

    "db": "064",
}

registers = {
    "RAX": "00", "EAX": "00", "AX": "00", "AH": "00", "AL": "00",
    "RBX": "01", "EBX": "01", "BX": "01", "BH": "01", "BL": "01",
    "RCX": "02", "ECX": "02", "CX": "02", "CH": "02", "CL": "02",
    "RDX": "03", "EDX": "03", "DX": "03", "DH": "03", "DL": "03",
    "RSI": "04", "ESI": "04", "SI": "04", "SIL": "04",
    "RDI": "05", "EDI": "05", "DI": "05", "DIL": "05",
    "RBP": "06", "EBP": "06", "BP": "06", "BPL": "06",
    "RSP": "07", "ESP": "07", "SP": "07", "SPL": "07",
    "R8": "08", "R8D": "08", "R8W": "08", "R8B": "08",
    "R9": "09", "R9D": "09", "R9W": "09", "R9B": "09",
    "R10": "10", "R10D": "10", "R10W": "10", "R10B": "10",
    "R11": "11", "R11D": "11", "R11W": "11", "R11B": "11",
    "R12": "12", "R12D": "12", "R12W": "12", "R12B": "12",
    "R13": "13", "R13D": "13", "R13W": "13", "R13B": "13",
    "R14": "14", "R14D": "14", "R14W": "14", "R14B": "14",
    "R15": "15", "R15D": "15", "R15W": "15", "R15B": "15",
    "CS": "16", 
    "DS": "17", 
    "ES": "18", 
    "SS": "19", 
    "FS": "20", 
    "GS": "21",
}

start_functions = [
    "_start", "start"
]

def getFileData(file):
    file_data = ""

    try:
        with open(file, "r") as file:
            file_data = file.read()
    except:
        print(f"{file} seems to be missing!")
        return None
    
    return file_data

def parse(data):
    bytes_parsed = ""
    functions = []
    labels = {}
    addresses = {}
    strings = []
    string_index = 0

    for line in data.split("\n"):
        is_string = False
        for character in line:
            if character == "'":
                is_string = not is_string
                if is_string:
                    strings.append("")
                continue

            if is_string:
                strings[len(strings) - 1] += character

    for line in data.split("\n"):
        is_comment = False
        is_section = False
        is_string = False

        for key in line.replace(",", "").split(" "):
            if ";" in key: is_comment = True
            if not is_comment:
                if key == '': continue
                if "'" in key:
                    is_string = not is_string

                    if is_string:
                        if strings[string_index] not in addresses:
                            addresses[strings[string_index]] = len(addresses) + 300
                        
                        functions[len(functions) - 1]["bytes"] += str(addresses[strings[string_index]])

                        string_index += 1
                    continue
                if is_string: continue
                if key == "section":
                    is_section = True
                    continue
                if is_section:
                    functions.append({"function": len(functions), "bytes": ""})
                    is_section = False
                    continue
                if key in operators:
                    function = operators[key]
                    if not function:
                        print(f"'{key}' is not supported and will be ignored")
                        is_comment = True
                    else:
                        functions[len(functions) - 1]["bytes"] += function
                elif key.upper() in registers:
                    functions[len(functions) - 1]["bytes"] += "2" + str(registers[key.upper()])
                elif ":" in key:
                    functions.append({"function": len(functions), "bytes": ""})
                    labels[key.replace(":", "")] = len(functions) - 1
                elif key in labels:
                    index = str(labels[key])
                    if len(index) == 1: index = "0" + index
                    functions[len(functions) - 1]["bytes"] += "1" + index
                elif "0x" in key:
                    if key not in addresses:
                        addresses[key] = len(addresses) + 300
                    
                    functions[len(functions) - 1]["bytes"] += str(addresses[key])
                elif key.isnumeric():
                    if key not in addresses:
                        addresses[key] = len(addresses) + 300
                    
                    functions[len(functions) - 1]["bytes"] += str(addresses[key])
                elif key in start_functions:
                    functions[len(functions) - 1]["bytes"] += "000"
                else:
                    print(f"'{key}' is not supported and will be ignored")

    start_found = None
    for label in labels:
        if label in start_functions:
            start_found = labels[label]
    if start_found == None:
        print("No start found, defaulting to 000")
        start_found = 0

    start_found = str(start_found)
    if len(start_found) == 1:
        start_found = "00" + start_found
    if len(start_found) == 2:
        start_found = "0" + start_found
    bytes_parsed += start_found

    for function in functions:
        bytes_parsed += "fun" + function["bytes"]
        print(function)
    
    bytes_parsed += "adr"
    for address in addresses:
        bytes_parsed += address + ":"

    return bytes_parsed