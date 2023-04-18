# PVS 2 Rust PoC
# Translates the code from IR.lisp to out.rs
# Nathan Gasc - SRI International 

# dependencies : Python3, prettier with rust plugin
 
# il va falloir faire une meilleure gestion des fonctions avec des closures
# puis faudra voir comment on gere les arrays et les refs
# polymorphism

#(recordtype
#    ((=> (project_1 project_192) (subrange 0 * nil nil))
#     (=> (project_2 project_293) (subrange 0 * nil nil))))
# tuple avec projection

import os
from IRparser import *
from language import *


if __name__ == "__main__":
    fichier = open("IR.lisp", 'r')
    src = fichier.read()
    fichier.close()

    #uses parser to go from lisp with parenthesis, to the same but in an array structure
    parsed = get_els_from_str(src) 

    #actual translation
    header = "use rug::Integer;\n"
    rust = "use rug::Integer;\nfn main(){let f = " + get_expr(parsed, []).toRust() + ";}"

    fichier = open("out.rs", "w")
    fichier.write(rust)
    fichier.close()

    os.system("prettier --write out.rs") # requires prettier

