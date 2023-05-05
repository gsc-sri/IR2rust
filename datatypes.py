from language_types import *

#(hello__btree_adt : (adt-recordtype
#                     ((=>
#                       (hello__btree_adt_index
#                        hello__btree_adt_index4056)
#                       (subrange 0 1 nil nil)))
#                     constructors
#                     ((hello__leaf)
#                      (hello__node hello__val hello__left
#                       hello__right))))

class datatype:
    def __init__(self, code) -> None:
        self.code : list = code
        self.name : str = code[1].strip(' \n')

        self.out : str = "trait " + self.name + " {fn ord(&self) -> i32 {0}}\n"

        adtRecordtype = code[2]
        constructors = adtRecordtype[2]

        i = 1
        for constructor in constructors:
            name = constructor[0]
            self.out += "struct " + name + "{\n"
            for el in constructors[1:]:
                pass
                # il nous manque le type de chaque element !
            self.out += "}\n"
            self.out += "impl " + self.name + " for " + name 
            self.out += " {fn ord(&self) -> i32 {" + str(i) + "}}\n"
            i += 1

