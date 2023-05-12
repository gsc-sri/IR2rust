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
        self.out += "trait " + self.name + "_trait {"
        for constructor in self.code:
            cname = constructor[1]

            # recognizer function
            self.out += "fn " + cname + "p (self : Self) -> bool;\n"
            DATATYPE_FUNCTIONS.append(cname + "p")

            # accessor functions
            for accessor in constructor[2:]:
                self.out += "fn " + accessor[1] + "(self : Self) -> " + get_type(accessor[2]) + ";\n"
                DATATYPE_FUNCTIONS.append(accessor[1])
            
            # update functions
            for accessor in constructor[2:]:
                self.out += "fn " + accessor[1] + "__update" 
                self.out += "(self : Self, "+ accessor[1] + " : " + get_type(accessor[2]) +") -> "+ self.name +" ;\n"
                DATATYPE_FUNCTIONS.append(accessor[1] + "__update" )

            # constructors
            self.out += "fn " + self.name + "__" + cname + "("
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + get_type(accessor[2]) + ","
            self.out += ") -> " + self.name + " {\n"
            self.out += self.name + "{\n"
            for cons2 in self.code:
                c2name = cons2[1]
                if c2name == cname:
                    self.out += "is__" + cname + " : true,\n"
                    for accessor in cons2[2:]:
                        self.out += accessor[1] + " : Some(Rc::new(" + accessor[1] + ")),\n"
                else :
                    self.out += "is__" + c2name + " : false,\n"
                    for accessor in cons2[2:]:
                        self.out += accessor[1] + " : None,\n"
            self.out += "}\n}\n"
            DATATYPE_FUNCTIONS.append(self.name + "__" + cname)

        self.out += "}\n\n"

        # --- STRUCT  ---

        self.out += "#[derive(Clone, PartialEq, Debug)]\nstruct "
        self.out += self.name + " {\n"
        for constructor in self.code:
            self.out += "is__" + constructor[1] + " : bool,\n"
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : Option<Rc<" + get_type(accessor[2]) + ">>,\n}\n\n"
        

        # --- IMPLEMENTATION ---

        self.out += "impl " + self.name + "_trait for " + self.name + "{\n"
        for constructor in self.code:
            
            cname = constructor[1]

            # recognizer function
            self.out += "fn " + cname + "p (self : Self) -> bool {self.is__"+ cname +"}\n"

            # accessor functions
            for accessor in constructor[2:]:
                self.out += "fn " + accessor[1] + "(self : Self) -> " + get_type(accessor[2]) + "{\n"
                self.out += "Rc_unwrap_or_clone(self."+ accessor[1] +".unwrap())}\n"
            
            # update functions
            for accessor in constructor[2:]:
                self.out += "fn " + accessor[1] + "__update" 
                self.out += "(self : Self, "+ accessor[1] + " : " + get_type(accessor[2]) +") -> "+ self.name +" {\n"
                self.out += "let mut updated = self.clone();\n"
                self.out += "updated."+ accessor[1] +" = Some(Rc::new("+ accessor[1] +"));updated\n}\n"

        self.out += "}\n\n"


    def toRust(self):
        return self.out

