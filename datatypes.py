from language_types import *

# [ "btree_adt__recognize__leafp", ... ]

class datatype:
    def __init__(self, code, name, theory) -> None:
        self.code : list = code
        self.name : str = name
        self.theory : str = theory
        self.out : str = ""
        global DATATYPES
        DATATYPES.append(name)
        global FUNCTIONS

        # Unpacking
        while isinstance(self.code[0][0], list): self.code = self.code[0]

        # if not shared, we should unpack the enum (unsafe to be faster ?)
        # https://rust-lang.github.io/unsafe-code-guidelines/layout/enums.html
        # note that the size of the datatype will be of the bigger possibility:
        # https://doc.rust-lang.org/reference/items/unions.html

        # --- ENUM CONSTRUCTION ---

        self.out += "#[derive(Clone, PartialEq, Eq, PartialOrd, Ord)]\nenum " + self.name + "{"
        for constructor in self.code:
            self.out += constructor[1] + "("+ constructor[1] +"),\n"
        self.out += "}\n\n"

        # --- STRUCTS CONSTRUCTION ---

        for constructor in self.code:
            self.out += "#[derive(Clone, PartialEq, Eq, PartialOrd, Ord)]\nstruct " + constructor[1] + " {\n"
            for accessor in constructor[2:]:
                self.out += accessor[1] + ": Rc<" + get_type(accessor[2]).toRust() + ">,\n"
            self.out += "}\n\n"

        # --- CONSTRUCTORS ---

        for constructor in self.code:
            self.out += "fn " + self.name + "__" + constructor[1] + "("
            argTypeList : list[typ] = []
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + get_type(accessor[2]).toRust() + ","
                argTypeList.append(get_type(accessor[2]))
            self.out += ") -> " + self.name + " {\n"
            self.out += self.name + "::" + constructor[1] + "(" + constructor[1] + "{"
            for accessor in constructor[2:]:
                self.out += accessor[1] + ": Rc::new(" + accessor[1] + "),"
            self.out += "})\n}\n\n"
            FUNCTIONS.append(Tfunction(None, self.name + "__" + constructor[1], [argTypeList, Tdatatype(None, self.name)]))

        # --- RECOGNIZERS ---
        
        for constructor in self.code:
            self.out += "fn " + self.theory + "__" + constructor[1] + "p (arg : "+ self.name +") -> bool {"
            self.out += "match arg {\n"
            for cons in self.code:
                if cons[1] == constructor[1]:
                    self.out += self.name + "::" + cons[1] + "(ref " + cons[1] + ") => true,\n"
                else:
                    self.out += self.name + "::" + cons[1] + "(ref " + cons[1] + ") => false,\n"
            self.out += "}\n}\n\n"
            FUNCTIONS.append(Tfunction(None, self.theory + "__" + constructor[1] + "p", [[Tdatatype(None, self.name)], Tbool]))

        # --- ACCESSORS --- 

        for constructor in self.code:
            for accessor in constructor[2:]:
                if self.name + "__" + accessor[1] in getFnNames():
                    print("DEBUG >> " + self.name + "__" + accessor[1] + " already found.") # info
                else:
                    self.out += "fn " + self.name + "__" + accessor[1] + "<T> (arg : "+ self.name +") -> T {"
                    self.out += "match arg {\n"
                    for cons in self.code:
                        accessors_cons = cons[2:]
                        if accessor in accessors_cons:
                            self.out += self.name + "::" + cons[1] + "(ref " + cons[1] + ") => unsafe{std::mem::transmute_copy(&Rc_unwrap_or_clone("+ cons[1] + "." + accessor[1] +".clone()))},\n"
                    self.out += "_ => unreachable!()\n"
                    self.out += "}\n}\n\n"
                    FUNCTIONS.append(Tfunction(None, self.name + "__" + accessor[1], [[Tdatatype(None, self.name)], Tgeneric(None)]))

        # --- UPDATE FUNCTIONS ---

        for constructor in self.code:
            for accessor in constructor[2:]:
                if self.name + "__" + accessor[1] + "__update" in getFnNames():
                    print("DEBUG >> " + self.name + "__" + accessor[1] + "__update already found.") # info
                else :
                    self.out += "fn " + self.name + "__" + accessor[1] + "__update<T> (arg : " + self.name + ", "
                    self.out += accessor[1] + ": T) -> "+ self.name +" {"
                    self.out += "match arg {\n"
                    for cons in self.code:
                        accessors_cons = cons[2:]
                        if accessor in accessors_cons:
                            self.out += self.name + "::" + cons[1] + "(ref " + cons[1] + ") => "+ self.name + "::" + cons[1] +"(" + cons[1] + "{"
                            for acc in cons[2:]:
                                if acc[1] == accessor[1]:
                                    self.out += acc[1] + ": Rc::new( unsafe{std::mem::transmute_copy(&"+ accessor[1] +")}),"
                                else:
                                    self.out += acc[1] + ": " + cons[1] + "." + acc[1] + ".clone(),"
                            self.out +=  "}),\n"
                    self.out += "_ => unreachable!()\n"
                    self.out += "}\n}\n\n"
                    FUNCTIONS.append(Tfunction(None, self.name + "__" + accessor[1] + "__update", [[Tdatatype(None, self.name), Tgeneric(None)], Tdatatype(None, self.name)]))


    def toRust(self):
        return self.out

