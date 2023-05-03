
#(hello__pt : (recordtype
#              ((=> (x x131) (subrange 0 * nil nil))
#               (=> (y y132) (subrange 0 * nil nil)))))
#hello__bwaa_adt : (subrange 0 2 nil nil)

TYPE_DECLARATIONS = "" # will be modified by get_type to add type declaration
# eg "type hello__bwaa_adt = i32;\n"
CUSTOM_TYPES = [] # ["hello__pt", "hello__bwaa_adt"] 

def getTypeDecl():
    global TYPE_DECLARATIONS
    return TYPE_DECLARATIONS

def create_type(name : str, code : str | list) -> None:
    global TYPE_DECLARATIONS
    if isinstance(code, list) and isinstance(code[0], str) and code[0].strip(" \n") == "recordtype":
        out = "#[derive(Clone)]\nstruct " + name + "{\n"
        for arg in code[1]:
            assert(arg[0].strip(" \n") == "=>")
            ident, uniqueIdent = arg[1]
            entryType = get_type(arg[2])
            out += ident + " : " + entryType + ",\n"
        out += "}"
    else:
        rhs = get_type(code)
        out = "type " + name + " = " + rhs + ";\n"

    TYPE_DECLARATIONS += out + "\n"

def get_type(t : str | list) -> str:
    # Get rust type from IR type string or array
    if isinstance(t, str):
        t = t.strip(" \n")
        if t == "mpq":
            print("W >> float found, trying integer")
            return "i32"
        elif t == "bool" or t == "boolean":
            return "bool"
        else:
            raise Exception("E >> unknown type :", t, ", trying i32\n")
    else:
        if t[0].strip(" \n") == "subrange":
            if t[1].strip(" \n") == '*':
                return 'nat'
            elif int(t[1]) >= 0:
                return 'i32'  # posnat
            else:
                return 'i32'
        elif t[0].strip(" \n") == "->":
            argtype = get_type(t[1])
            outtype = get_type(t[2])
            return "Box<dyn Fn(" + argtype + ") -> " + outtype + ">"
        elif t[0].strip(" \n") == "array":
            arrayType = get_type(t[1])
            size, high = t[2].strip(' \n[]').split("/")
            return "Rc<[" + arrayType + "; " + size + "]>"
        elif isinstance(t[1], str) and t[1].strip(' \n') == ":":
            # custom type
            name = t[0].strip("\n")
            global CUSTOM_TYPES
            if name in CUSTOM_TYPES:
                return name
            else:
                create_type(name, t[2])
                CUSTOM_TYPES.append(name)
                return name
        else:
            raise Exception("E >> UKWN TYPE : ", t)


def isArray(code):
    if not isinstance(code, list):
        return False
    key = code[0].strip(' \n')
    if key == "last" or key[:4] == "ivar":
        return isArray(code[1])
    elif key == "array":
        return True
    elif key in CUSTOM_TYPES:
        return isArray(code[2])
    else:
        return False
    
def isRecordtype(code):
    if not isinstance(code, list):
        return False
    key = code[0].strip(' \n')
    if key == "last" or key[:4] == "ivar":
        return isRecordtype(code[1])
    elif key == "recordtype":
        return True
    elif key in CUSTOM_TYPES:
        return isRecordtype(code[2])
    else:
        return False