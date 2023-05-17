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
        

        # --- TRAIT CONSTRUCTION ---
        self.out += "trait " + self.name + "_trait {"
        i = 0
        for constructor in self.code:
            cname = constructor[1]

            # recognizer function
            self.out += "fn " + self.theory + "__" + cname + "p (self : Self) -> bool;\n"
            DATATYPE_FUNCTIONS.append(self.theory + "__" + cname + "p")

            # accessor functions
            for accessor in constructor[2:]:
                self.out += "fn " + self.name + "__" + accessor[1] + "(self : Self) -> " + get_type(accessor[2]).toRust() + ";\n"
                DATATYPE_FUNCTIONS.append(self.name + "__" + accessor[1])
            
            # update functions
            for accessor in constructor[2:]:
                self.out += "fn " + self.name + "__" + accessor[1] + "__update" 
                self.out += "(self : Self, "+ accessor[1] + " : " + get_type(accessor[2]).toRust() +") -> "+ self.name +" ;\n"
                DATATYPE_FUNCTIONS.append(self.name + "__" + accessor[1] + "__update" )

            # constructors
            self.out += "fn " + self.name + "__" + cname + "("
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + get_type(accessor[2]).toRust() + ","
            self.out += ") -> " + self.name + " {\n"
            self.out += self.name + " {\n"
            self.out += "ord : " + str(i) + ",\n"
            i += 1
            self.out += "data : Rc::new(" + cname + "{"
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + accessor[1] + ",\n"
            self.out += "})\n}\n}\n"
            DATATYPE_FUNCTIONS.append(self.name + "__" + cname)

        self.out += "}\n\n"

        # --- STRUCTS  ---

        self.out += "#[derive(Clone, Debug)]\nstruct "
        self.out += self.name + " {\n"
        self.out += "ord : i32,\n data : Rc<dyn Any>\n}"

        for constructor in self.code:
            self.out += "#[derive(Clone, PartialEq, Debug)]\n"
            self.out += "struct " + constructor[1] + " {\n"
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + get_type(accessor[2]).toRust() + ",\n"
            self.out += "}\n\n"
        

        # --- IMPLEMENTATIONS ---

        # PartialEq for our main trait
        self.out += "impl PartialEq for " + self.name + " {\nfn eq(&self, other: &Self) -> bool {\n"
        self.out += "if self.ord == other.ord {"
        i = 0
        for constructor in self.code:
            self.out += "if self.ord == " + str(i) + " {\n"
            self.out += "return Rc::downcast::<"+constructor[1]+">(self.data.clone()).unwrap() == Rc::downcast::<"+constructor[1]+">(other.data.clone()).unwrap()}\n"
            i+=1
        self.out += "}\nfalse}\n}\n\n"


        # our trait for out object
        self.out += "impl " + self.name + "_trait for " + self.name + "{\n"
        i = 0
        for constructor in self.code:
            
            cname = constructor[1]

            # recognizer function
            self.out += "fn " + self.theory + "__" + cname + "p (self : Self) -> bool {self.ord == "+ str(i) +"}\n"
            

            # accessor functions
            for accessor in constructor[2:]:
                self.out += "fn " + self.name + "__" + accessor[1] + "(self : Self) -> " + get_type(accessor[2]).toRust() + "{\n"
                self.out += "Rc_unwrap_or_clone(Rc::downcast::<"+ constructor[1] +">(self.data).unwrap())." + accessor[1] + "}\n"
            
            # update functions
            for accessor in constructor[2:]:
                self.out += "fn " + self.name + "__" + accessor[1] + "__update" 
                self.out += "(self : Self, "+ accessor[1] + " : " + get_type(accessor[2]).toRust() +") -> "+ self.name +" {\n"
                self.out += "let mut updated = Rc::downcast::<"+ constructor[1] +">(self.data).unwrap();\n"
                self.out += "Rc::make_mut(&mut updated)." + accessor[1] + " = " + accessor[1] + ";\n"
                self.out += self.name + " { ord: " + str(i) + ", data : updated}\n}\n "
            i += 1
        self.out += "}\n\n"


    def toRust(self):
        return self.out

