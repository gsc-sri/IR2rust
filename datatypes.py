from language_types import *

DATATYPE_FUNCTIONS = []
# [ "btree_adt__recognize__leafp", ... ]

class datatype:
    def __init__(self, code, name, theory) -> None:
        self.code : list = code
        self.name : str = name
        self.theory : str = theory
        self.out : str = ""
        global DATATYPES
        DATATYPES.append(name)
        global DATATYPE_FUNCTIONS

        # Unpacking
        while isinstance(self.code[0][0], list): self.code = self.code[0]

        # Use the format theory__accessor__rustType
        # ie btree__val__i32 
        # if shared , ie same accessor same type , we should match the enum 
        # if not shared, we should unpack the enum (unsafe to be faster ?)
        # https://rust-lang.github.io/unsafe-code-guidelines/layout/enums.html
        # note that the size of the datatype will be of the bigger possibility:
        # https://doc.rust-lang.org/reference/items/unions.html
        # we will probably need an accessor operator

        # apres faudra revenir au flameggraph de la rpz en fonction des arrays
        # change panic! to unreachable!

        # --- ENUM CONSTRUCTION ---

        self.out += "#[derive(Clone, PartialEq)]\nenum " + self.name + "{"
        for constructor in self.code:
            self.out += constructor[1] + "("+ constructor[1] +"),\n"
        self.out += "}\n\n"

        # --- STRUCTS CONSTRUCTION ---

        for constructor in self.code:
            self.out += "#[derive(Clone, PartialEq)]\nstruct " + constructor[1] + " {\n"
            for accessor in constructor[2:]:
                self.out += accessor[1] + ": Rc<" + get_type(accessor[2]).toRust() + ">,\n"
            self.out += "}\n\n"

        # --- CONSTRUCTORS ---

        for constructor in self.code:
            self.out += "fn " + self.name + "__" + constructor[1] + "("
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + get_type(accessor[2]).toRust() + ","
            self.out += ") -> " + self.name + " {\n"
            self.out += self.name + "::" + constructor[1] + "(" + constructor[1] + "{"
            for accessor in constructor[2:]:
                self.out += accessor[1] + ": Rc::new(" + accessor[1] + "),"
            self.out += "})\n}\n\n"
            DATATYPE_FUNCTIONS.append(self.name + "__" + constructor[1])

        # --- RECOGNIZERS ---
        
        for constructor in self.code:
            self.out += "fn " + self.theory + "__" + constructor[1] + "p (a : "+ self.name +") -> bool {"
            self.out += "match a {\n"
            for cons in self.code:
                if cons[1] == constructor[1]:
                    self.out += self.name + "::" + cons[1] + "(ref " + cons[1] + ") => true,\n"
                else:
                    self.out += self.name + "::" + cons[1] + "(ref " + cons[1] + ") => false,\n"
            self.out += "}\n}\n\n"
            DATATYPE_FUNCTIONS.append(self.theory + "__" + constructor[1] + "p")

        # --- ACCESSORS --- 

        for constructor in self.code:
            for accessor in constructor[2:]:
                if self.name + "__" + accessor[1] in DATATYPE_FUNCTIONS:
                    print("DEBUG >> " + self.name + "__" + accessor[1] + " already found.") # info
                else:
                    self.out += "fn " + self.name + "__" + accessor[1] + "<T> (a : "+ self.name +") -> T {"
                    self.out += "match a {\n"
                    for cons in self.code:
                        accessors_cons = cons[2:]
                        if accessor in accessors_cons:
                            self.out += self.name + "::" + cons[1] + "(ref " + cons[1] + ") => unsafe{std::mem::transmute_copy(&Rc_unwrap_or_clone("+ cons[1] + "." + accessor[1] +".clone()))},\n"
                    self.out += "_ => unreachable!()\n"
                    self.out += "}\n}\n\n"
                    DATATYPE_FUNCTIONS.append(self.name + "__" + accessor[1])

        # --- UPDATE FUNCTIONS ---

        for constructor in self.code:
            for accessor in constructor[2:]:
                if self.name + "__" + accessor[1] + "__update" in DATATYPE_FUNCTIONS:
                    print("DEBUG >> " + self.name + "__" + accessor[1] + "__update already found.") # info
                else :
                    self.out += "fn " + self.name + "__" + accessor[1] + "__update<T> (a : " + self.name + ", "
                    self.out += accessor[1] + ": T) -> "+ self.name +" {"
                    self.out += "match a {\n"
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
                    DATATYPE_FUNCTIONS.append(self.name + "__" + accessor[1] + "__update" )


    def toRust(self):
        return self.out

