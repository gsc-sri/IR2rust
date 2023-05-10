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
            self.out += "fn " + cname + "p (self : Rc<Self>) -> bool;\n"
            DATATYPE_FUNCTIONS.append(cname + "p")

            # accessor functions
            for accessor in constructor[2:]:
                self.out += "fn " + accessor[1] + "(self : Rc<Self>) -> " + get_type(accessor[2]) + ";\n"
                DATATYPE_FUNCTIONS.append(accessor[1])
            
            # update functions
            for accessor in constructor[2:]:
                self.out += "fn " + accessor[1] + "__update" 
                self.out += "(self : Rc<Self>, "+ accessor[1] + " : " + get_type(accessor[2]) +") -> Rc<dyn "+ self.name +"> ;\n"
                DATATYPE_FUNCTIONS.append(accessor[1] + "__update" )

        # ord function
        self.out += "fn "+ self.name + "__" + "ord(self : Rc<Self>) -> i32;\n"
        DATATYPE_FUNCTIONS.append(self.name + "__" + "ord")
        self.out += "}\n\n"

        # WIP functions
        self.out += "fn btree_adt__subterm(a : Rc<dyn "+ self.name +">, b : Rc<dyn "+ self.name +">) -> bool {"
        self.out += 'panic!("Subterm is not implemented yet")}\n\n'

        self.out += "fn btree_adt__doublelessp(a : Rc<dyn "+ self.name +">, b : Rc<dyn "+ self.name +">) -> bool {"
        self.out += 'panic!("<< is not implemented yet")}\n\n'

        # --- CONSTRUCTORS ---
        # These are functions outside trait because they make it bug # TODO : investigate
        for constructor in self.code:
            cname = constructor[1]
            self.out += "fn " + self.name + "__" + cname + "("
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + get_type(accessor[2]) + ",\n"
            self.out += ") -> Rc<" + cname + "> {\nRc::new("
            self.out += cname + " {"
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + accessor[1] + ",\n"
            self.out += "})\n}\n\n"
            #DATATYPE_FUNCTIONS.append(self.name + "__" + cname)
            #Do not add to the list of fn because regular call

        # --- STRUCTS  ---

        for constructor in self.code:
            self.out += "#[derive(Clone)]\nstruct " + constructor[1] + " {\n"
            for accessor in constructor[2:]:
                self.out += accessor[1] + " : " + get_type(accessor[2]) + ",\n"
            self.out += "}\n\n"

        # --- IMPLEMENTATIONS ---

        i = 1 # for ord
        for constructor in self.code:
            self.out += "impl " + self.name + " for " + constructor[1] + "{\n"
            self.out += "fn "+ self.name + "__" +"ord(self : Rc<Self>) -> i32 {" + str(i) + "}"
            i += 1
            thisname = constructor[1]

            for constructor2 in self.code:            
                cname = constructor2[1]

                # recognizer function
                if cname == thisname:
                    self.out += "fn " + cname + "p (self : Rc<Self>) -> bool {true}\n"
                else :
                    self.out += "fn " + cname + "p (self : Rc<Self>) -> bool {false}\n"

                # accessor functions
                if cname == thisname:
                    for accessor in constructor2[2:]:
                        self.out += "fn " + accessor[1] + "(self : Rc<Self>) -> " + get_type(accessor[2]) + "{"
                        self.out += "self." + accessor[1] 
                        if isinstance(accessor[2], list) and accessor[2][0] in DATATYPES:
                            self.out += ".clone()}\n"
                        else:
                            self.out += "}\n"
                else:
                    # Should never be called, if so we panic
                    for accessor in constructor2[2:]:
                        self.out += "fn " + accessor[1] + "(self : Rc<Self>) -> " + get_type(accessor[2]) + "{panic!()}\n"
                
                # update functions
                if cname == thisname:
                    for accessor in constructor2[2:]:
                        self.out += "fn " + accessor[1] + "__update"  
                        self.out += "(self : Rc<Self>, "+ accessor[1] + " : " + get_type(accessor[2]) +") -> Rc<dyn "+ self.name +"> {"
                        self.out += "let mut updated: Rc<"+ thisname +"> = self.clone();"
                        self.out += "(*Rc::make_mut(&mut updated))."+ accessor[1] +" = "+ accessor[1] +";"
                        self.out += "updated }\n"
                else:
                    # Should not be called too
                    for accessor in constructor2[2:]:
                        self.out += "fn " + accessor[1] + "__update" 
                        self.out += "(self : Rc<Self>, "+ accessor[1] + " : " + get_type(accessor[2]) + ") -> Rc<dyn "+ self.name +"> {panic!()}\n"

            self.out += "}\n\n"


    def toRust(self):
        return self.out

