from language_types import *

DATATYPE_FUNCTIONS = []
# [ "btree_adt__recognize__leafp", ... ]

class datatype:
    def __init__(self, code, name) -> None:
        self.code : list = code
        self.name : str = name
        self.out : str = ""
        global DATATYPES
        DATATYPES.append(name)
        global DATATYPE_FUNCTIONS

        # Unpacking
        while isinstance(self.code[0][0], list): self.code = self.code[0]
        
        # --- TRAIT CONSTRUCTION ---
        self.out += "trait " + self.name + " {"
        for constructor in self.code:
            cname = constructor[1]

            # recognizer function
            self.out += "fn " + self.name + "__recognize__" + cname + "p (&self) -> bool;\n"
            DATATYPE_FUNCTIONS.append(self.name + "__recognize__" + cname)

            # accessor functions
            for accessor in constructor[2:]:
                self.out += "fn " + accessor[1] + "(&self) -> " + get_type(accessor[2], True) + ";\n"
                DATATYPE_FUNCTIONS.append(self.name + "__" + accessor[1])
            
            # update functions
            for accessor in constructor[2:]:
                self.out += "fn " + self.name + "__update__" + accessor[1] 
                self.out += "(&mut self, "+ accessor[1] + " : " + get_type(accessor[2], True) +");\n"
                DATATYPE_FUNCTIONS.append(self.name + "__update__" + accessor[1])

        # ord function
        self.out += "fn "+ self.name + "__" + "ord(&self) -> i32;\n"
        DATATYPE_FUNCTIONS.append(self.name + "__" + "ord")
        self.out += "}\n"

        # --- CONSTRUCTORS ---
        # These are functions outside trait because they make it bug # TODO : investigate
        for constructor in self.code:
            cname = constructor[1]
            self.out += "fn " + self.name + "__" + cname + "("
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + get_type(accessor[2], True) + ",\n"
            self.out += ") -> " + cname + "{\n"
            self.out += cname + " {"
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + accessor[1] + ",\n"
            self.out += "}\n}\n"
            DATATYPE_FUNCTIONS.append(self.name + "__" + cname)

        # --- STRUCTS  ---

        for constructor in self.code:
            self.out += "struct " + constructor[1] + " {\n"
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + get_type(accessor[2], True) + ",\n"
            self.out += "}\n"

        # --- IMPLEMENTATIONS ---

        i = 1 # for ord
        for constructor in self.code:
            self.out += "impl " + self.name + " for " + constructor[1] + "{\n"
            self.out += "fn "+ self.name + "__" +"ord(&self) -> i32 {" + str(i) + "}"
            i += 1
            thisname = constructor[1]

            for constructor2 in self.code:            
                cname = constructor2[1]

                # recognizer function
                if cname == thisname:
                    self.out += "fn " + self.name + "__recognize__" + cname + "p (&self) -> bool {true}\n"
                else :
                    self.out += "fn " + self.name + "__recognize__" + cname + "p (&self) -> bool {false}\n"

                # accessor functions
                if cname == thisname:
                    for accessor in constructor2[2:]:
                        self.out += "fn " + accessor[1] + "(&self) -> " + get_type(accessor[2], True) + "{"
                        self.out += "self." + accessor[1] 
                        if isinstance(accessor[2], list) and accessor[2][0] in DATATYPES:
                            self.out += ".clone()}\n"
                        else:
                            self.out += "}\n"
                else:
                    # Should never be called, if so we panic
                    for accessor in constructor2[2:]:
                        self.out += "fn " + accessor[1] + "(&self) -> " + get_type(accessor[2], True) + "{panic!()}\n"
                
                # update functions
                if cname == thisname:
                    for accessor in constructor2[2:]:
                        self.out += "fn " + self.name + "__update__" + accessor[1] 
                        self.out += "(&mut self, "+ accessor[1] + " : " + get_type(accessor[2], True) +"){"
                        self.out += "self." + accessor[1] + " = " + accessor[1] + ";}\n"
                else:
                    # Should not be called too
                    for accessor in constructor2[2:]:
                        self.out += "fn " + self.name + "__update__" + accessor[1] 
                        self.out += "(&mut self, "+ accessor[1] + " : " + get_type(accessor[2], True) + "){panic!()}\n"

            self.out += "}\n"


    def toRust(self):
        return self.out

