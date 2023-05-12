
#(hello__pt : (recordtype
#              ((=> (x x131) (subrange 0 * nil nil))
#               (=> (y y132) (subrange 0 * nil nil)))))
#hello__bwaa_adt : (subrange 0 2 nil nil)

TYPE_DECLARATIONS = "" # will be modified by get_type to add type declaration
# eg "type hello__bwaa_adt = i32;\n"
CUSTOM_TYPES = [] # ["hello__pt", "hello__bwaa_adt"] 
DATATYPES = []
RECORDS = []

def getTypeDecl():
    global TYPE_DECLARATIONS
    return TYPE_DECLARATIONS

def create_type(name : str, code : str | list) -> None:
    #On first time reading a typename, we add it to our list
    #and create corresponding Rust type
    global TYPE_DECLARATIONS
    global CUSTOM_TYPES

    # --- RECORD ---
    if isinstance(code, list) and isinstance(code[0], str) and code[0].strip(" \n") == "recordtype":
        rec = record(code, name)

        out = "#[derive(Clone)]\nstruct " + name + "{\n"
        for field in rec.fields:
            out += field[0] + " : " + field[1] + ",\n"
        out += "}"

    # --- TYPE ---
    else:
        rhs = get_type(code)
        out = "type " + name + " = " + rhs + ";\n"
        CUSTOM_TYPES.append(name)

    TYPE_DECLARATIONS += out + "\n"


class record:
    def __init__(self, code : list, name = "") -> None:
        self.name : str = name
        self.code : list = code
        assert(code[0].strip(" \n") == "recordtype")
        self.fields : list = []
        for entry in code[1]:
            assert(entry[0].strip(" \n") == "=>")
            ident, uniqueIdent = entry[1]
            entryType = get_type(entry[2])
            self.fields.append([ident, entryType])

        global RECORDS
        # We need to have a name before returning
        if self.name == "":
            for rec in RECORDS:
                if self == rec:
                    self.name = rec.name
                    return
            # We are not in RECORDS
            self.name = "record_" + str(len(RECORDS))
        # else no problem a name has been given

    def __eq__(self, code : list): # TODO : improve with use of self.fields
        a = "".join(self.code).replace(" \n", "")
        b = "".join(code).replace(" \n", "")
        return a == b
    

def get_type(t : str | list) -> str:
    # Get rust type from IR type string or array

    if isinstance(t, str):
        t = t.strip(" \n")

        # --- REALS ---
        if t == "mpq":
            print("W >> float found, trying integer")
            return "i32"
        
        # --- BOOLS ---
        elif t == "bool" or t == "boolean":
            return "bool"
        
        # --- UKN STR TYPE ---
        else:
            raise Exception("E >> unknown type :", t, ", trying i32\n")
        
    else:

        # --- INTEGERS ---
        if t[0].strip(" \n") == "subrange":
            return 'i32'
        
        # --- FUNTYPES ---
        elif t[0].strip(" \n") == "->":
            argtype = get_type(t[1])
            outtype = get_type(t[2])
            return "Box<dyn Fn(" + argtype + ") -> " + outtype + ">"
        
        # --- ARRAYS ---
        elif t[0].strip(" \n") == "array":
            arrayType = get_type(t[1])
            size, high = t[2].strip(' \n[]').split("/")
            return "Rc<[" + arrayType + "; " + size + "]>"
        
        # --- RECORD ---    
        elif t[0].strip(" \n") == "recordtype":
            rec = record(t)
            return rec.name
        
        # --- TYPENAMES ---
        elif isinstance(t[1], str) and t[1].strip(' \n') == ":":
            # custom type
            name = t[0].strip("\n")
            global CUSTOM_TYPES
            global DATATYPES
            global RECORDS
            if name in CUSTOM_TYPES:
                return name
            elif name in DATATYPES:
                return name
            else:
                for rec in RECORDS:
                    if name == rec.name:
                        return name
                create_type(name, t[2])
                return name

        # --- UKN ARRAY TYPE ---
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