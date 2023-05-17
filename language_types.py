
#(hello__pt : (recordtype
#              ((=> (x x131) (subrange 0 * nil nil))
#               (=> (y y132) (subrange 0 * nil nil)))))
#hello__bwaa_adt : (subrange 0 2 nil nil)

TYPE_DECLARATIONS = "" # will be modified by get_type to add type declaration
# eg "type hello__bwaa_adt = i32;\n"
CUSTOM_TYPES : list = [] # ["hello__pt", "hello__bwaa_adt"] list[typ]
DATATYPES = ["ordstruct_adt__ordstruct_adt"]
RECORDS : list = [] #list[record]

def getTypeDecl():
    global TYPE_DECLARATIONS
    return TYPE_DECLARATIONS

class typ:
    def __init__(self, code : list) -> None:
        pass

    def toRust(self) -> str:
        pass

class Tint(typ):
    def __init__(self, code : list) -> None:
        self.code = code

    def toRust(self) -> str:
        return "i32"

class Treal(typ):
    def __init__(self, code : list) -> None:
        self.code = code

    def toRust(self) -> str:
        return "f32"

class Tbool(typ):
    def __init__(self, code : list) -> None:
        self.code = code

    def toRust(self) -> str:
        return "bool"

class Tfunction(typ):
    def __init__(self, code : list) -> None:
        self.code = code
        self.argtype = get_type(code[1])
        self.outtype = get_type(code[2])

    def toRust(self) -> str:
        return "Rc<dyn Fn(" + self.argtype + ") -> " + self.outtype + ">"

class Tarray(typ):
    def __init__(self, code : list) -> None:
        self.code = code
        self.arrayType : typ = get_type(code[1])
        self.size, self.high = code[2].strip(' \n[]').split("/")

    def toRust(self) -> str:
        return "Rc<[" + self.arrayType.toRust() + "; " + self.size + "]>"

class Trecord(typ):
    def __init__(self, code : list, name = "") -> None:
        self.name : str = name
        self.code : list = code

        self.fields : list = []
        for entry in code[1]:
            assert(entry[0].strip(" \n") == "=>")
            ident, uniqueIdent = entry[1]
            entryType : typ = get_type(entry[2])
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

            global TYPE_DECLARATIONS
            out = "#[derive(Clone)]\nstruct " + self.name + "{\n"
            for field in self.fields:
                out += field[0] + " : " + field[1] + ",\n"
            out += "}\n"
            RECORDS.append(self)
            TYPE_DECLARATIONS += out

    def __eq__(self, other): 
        code = other.code
        ret = (isinstance(self.code, list) and isinstance(code, list)
                and self.code[0] == 'recordtype'
                and code[0] == 'recordtype')
        if not ret : return ret
        ret &= len(code[1]) == len(self.code[1])
        if not ret : return ret
        for i in range(len(code[1])):
            f1 = self.code[1][i]
            f2 = code[1][i]
            ret &= f1[0] == '=>'
            if not ret : return ret
            ret &= f2[0] == '=>'
            if not ret : return ret
            ret &= f1[1][0] == f2[1][0]
            if not ret : return ret
            ret &= f1[2] == f2[2] 
            if not ret : return ret
        return ret

    def toRust(self) -> str:
        return self.name

class Tcustom(typ):
    def __init__(self, code : list) -> None:
        self.code = code
        self.name = code[0].strip("\n")
        global CUSTOM_TYPES
        global DATATYPES
        global RECORDS
        global TYPE_DECLARATIONS
        if self.name in [i.name for i in CUSTOM_TYPES]:
            j = [i.name for i in CUSTOM_TYPES].index(self.name)
            self.type = CUSTOM_TYPES[j].type
        elif not self.name in DATATYPES:
            if isinstance(self.code[2], list) and self.code[2][0] == "recordtype":
                for rec in RECORDS:
                    if self.name == rec.name:
                        return
                self.type = Trecord(self.code[2], self.name)
            else:
                self.type = get_type(self.code[2])
                out = "type " + self.name + " = " + self.type.toRust() + ";\n"
                CUSTOM_TYPES.append(self)
                TYPE_DECLARATIONS += out + "\n"
        else:
            self.type = None

    def toRust(self) -> str:
        return self.name




def get_type(t : str | list) -> str:
    # Get rust type from IR type string or array

    if isinstance(t, str):
        t = t.strip(" \n")
        if t == "mpq":
            #return Treal(t)
            return Tint(t)
        elif t == "bool" or t == "boolean":
            return Tbool(t)
        else:
            raise Exception("E >> unknown type :", t, ", trying i32\n")
        
    else:
        if t[0].strip(" \n") == "subrange":
            return Tint(t)
        elif t[0].strip(" \n") == "->":
            return Tfunction(t)
        elif t[0].strip(" \n") == "array":
            return Tarray(t)
        elif t[0].strip(" \n") == "recordtype":
            return Trecord(t)
        elif isinstance(t[1], str) and t[1].strip(' \n') == ":":
            return Tcustom(t)
        else:
            raise Exception("E >> UKWN TYPE : ", t)
