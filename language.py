
DEBUG = True

def debug(c:str) -> None: 
    if DEBUG:
        print("DEBUG >> " + c)

OPERATOR_CORR = {"+" : "+",
                 "-" : "-",
                 "*" : "*",
                 "/" : "/",
                 "nrem" : "%",
                 "=" : "==",
                 "<" : "<"
                 }

def get_type(t):
    # Get rust type from IR type string
    if isinstance(t, str):
        t = t.strip(" \n")
        if t == "mpq":
            debug("W >> float found, trying integer")
            return "Integer"
        elif t == "bool" or t == "boolean":
            return "bool"
        else:
            print("W >> unknown type :", t, ", trying Integer\n")
            return "Integer"
            raise Exception("UKNW STR TYPE : " + t)
    else:
        if t[0] == "subrange":
            if t[1] == '*':
                return 'nat'
            elif int(t[1]) >= 0:
                return 'Integer' #posnat
            else:
                return 'Integer'
        elif t[0] == "->":
            argtype = get_type(t[1])
            outtype = get_type(t[2])
            return "Box<dyn Fn(" + argtype + ") -> " + outtype + ">"
        elif t[0] == "recordtype":
            #TODO
            raise Exception("E >> TODO")
        elif t[0] == "array":
            arrayType = get_type(t[1])
            size, high = t[2].strip(' \n[]').split("/")
            return "[" + arrayType + ";" + size + "]"
        elif t[1].strip(' \n') == ":":
            # custom type
            return get_type(t[2]) #we try to guess the custom type
        else:
            raise Exception("E >> UKWN TYPE : ", t)


def get_var(v):
    # From parsed var return name and type
    # e.g. from ['last', ['ivar_1', ['subrange', '0', '*', 'nil', 'nil'], 'n']]
    # to [name='ivar_1', type='Integer']
    if v[0] == "last":
        return get_var(v[1])
    if isinstance(v, str):
        v = v.strip(' \n')
        if v.isdigit():
            return v, "Integer"
        else:
            raise Exception("E >> get_var error on : " + v)
    return v[0], get_type(v[1])


#### LANGUAGE ####

# env is an array looking like:
# [ [names, name, type, used ] ]
# eg [ [ ["ivar_1", "ivar_5"], "ivar_1", "Integer", True ] ]

class expr: 
    # abstract class for expressions (= everything)
    # the init must parse
    def __init__(self, code, env = []) -> None:
        raise Exception("Must implement __init__ function !")
    
    def toRust(self) -> str:
        raise Exception("Must implement toRust function !")
    
def get_expr(tabl, env) -> expr:
    # From ['object', ...] to corresponding expr
    if isinstance(tabl, str):
        return Evalue(tabl, env)
    try:
        key = tabl[0]
        if not isinstance(key, str): # handles cases such as [[ thing ]]
            if len(tabl) < 2:
                return get_expr(key, env)
            else:
                return Elambdacall(tabl, env)
        else:
            key = key.strip(' \n')
    except:
        raise Exception("E >> error getting expr from : " + str(tabl))

    if key == "lambda": return Efn(tabl, env)
    elif key == "let": return Elet(tabl, env)
    elif key == "if": return Eif(tabl, env)
    elif key == "release": return Erelease(tabl, env)
    elif key == "lett": return Elett(tabl, env)
    elif key == "lookup": return Elookup(tabl, env)
    elif key == "update": return Eupdate(tabl, env)
    elif key in OPERATOR_CORR.keys(): return Eoperator(tabl, env)
    elif key[:4] == "ivar" or key == "last": return Evariable(tabl, env)
    else:
        return Eappication(tabl, env)
        #raise Exception("E >> falling through parser with : " + str(tabl))


class Evariable(expr):
    # Representation of a variable with possibly a last before
    # Here is a representation for variables as expr ! Hence they
    # must already be in the env. For declaration see Elet and Efn
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        if not Evariable.isVariable(self.code):
            raise Exception("E >> can't parse variable : " + self.code)

        self.isLast = code[0].strip(' \n') == 'last'
        if self.isLast:
            self.code = self.code[1]

        self.name = self.code[0].strip(' \n')

        self.fromEnv = None
        for envVar in self.env:
            if self.name in envVar[0]:
                self.fromEnv = envVar 
                envVar[-1] = True
                break
        
        if self.fromEnv == None:
            raise Exception("E >> can't find variable " + self.name + " in env " + str(self.env))
        
        self.name = self.fromEnv[1]
        self.type = self.fromEnv[2]
        self.used = self.fromEnv[3]

        debug("Evariable : Fetched var "+ self.name + " of type " + self.type + " from env, used : " + str(self.used))

    def isVariable(arr) -> bool:
        try:
            if arr[0].strip(" \n") == "last":
                return Evariable.isVariable(arr[1])
            return True
        except:
            return False
    
    def toRust(self) -> str:
        if self.used and not self.isLast:
            return self.name + ".clone()"
        return self.name

class Evalue(expr):
    # Representation of a value sur as "123"
    def __init__(self, code, env = []) -> None:
        self.code = code.strip(' \n')
        self.env = env

        if not Evalue.isValue(self.code):
            raise Exception("E >> can't parse value : " + self.code)
        
        debug("Evalue : returning value " + code)

    def isValue(arr) -> bool:
        return arr.isdigit()
    
    def toRust(self) -> str:
        return "Integer::from(" + self.code + ")"
    
class Elambdacall(expr):
    # Representation of a lambda call: the first element is a var
    # containing a fn, the following are the arguments
    # TODO :
    #   Do some more checks 
    #   Handles > 1 args
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env
        
        debug("Elambdacall : calling lamda fn with arg: " + str(code[1]))
    
    def toRust(self) -> str:
        return get_expr(self.code[0], self.env).toRust() + "(" + get_expr(self.code[1], self.env).toRust()+")"

class Elet(expr):
    # Representation of a let. It changes the env with the new variable
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        self.varName = self.code[1].strip(' \n')
        self.varType = get_type(self.code[2])

        if isinstance(self.code[3], str) and self.code[3].strip(' \n') == 'nil':
            self.middle = None
            debug("WARN : cannot create null from nil [let " + self.varName+"]")
            self.env.append([[self.varName], self.varName, self.varType, False])
            self.right = get_expr(self.code[4], self.env)  
            if isinstance(self.right, Eupdate):
                debug("WARN : making exception : found update in that let. It will not be done")
            else:
                raise Exception("E >> found let "+self.varName+" = null")
        else:
            self.middle = get_expr(self.code[3], self.env)   
            self.env = self.middle.env
            self.env.append([[self.varName], self.varName, self.varType, False])
            self.right = get_expr(self.code[4], self.env)  

        debug("Elet : created let for variable " + self.varName)
    
    def toRust(self) -> str:
        if self.middle == None:
            # so we have an update to bypass:
            output = self.right.arrayName
        else:
            output = "let " + self.varName + " : " + self.varType 
            output += " = {" + self.middle.toRust()
            output += '};\n'
            output += self.right.toRust()
        return output
    
class Elett(expr):
    # Representation of a lett. It adds a new name for the variable in the env
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        self.varName = self.code[1].strip(' \n')
        self.varType = get_type(self.code[2])

        self.targetVar, t = get_var(self.code[4])

        for var in self.env:
            if self.targetVar in var[0]:
                var[0].append(self.varName)
                break

        debug("Elett : added name " + self.varName + " to var " + self.targetVar)
    
    def toRust(self) -> str:
        return get_expr(self.code[5], self.env).toRust()

class Eif(expr):
    # Representation of a if then else
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env
        debug("Eif : if stmt")
    
    def toRust(self) -> str:
        output = "if " + get_expr(self.code[1], self.env).toRust()
        output += "{" + get_expr(self.code[2], self.env).toRust() 
        output += "} else {" + get_expr(self.code[3], self.env).toRust() + "}"
        return output
    
class Erelease(expr):
    # Representation of a if then else
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env
        debug("Erelease : ignoring")
    
    def toRust(self) -> str:
        return get_expr(self.code[3], self.env).toRust()

class Elookup(expr):
    # Lookup of an array
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        self.arrayName, self.arrayType = get_var(self.code[1])

        debug("Elookup")
    
    def toRust(self) -> str:
        # we are forced to clone on lookup because we may be using the variable
        # that's not optimal but still good enough because its only one value
        return self.arrayName + "[(" + get_expr(self.code[2], self.env).toRust() + ").to_usize_wrapping()].clone()"

class Eupdate(expr):
    # Update of an array
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        self.arrayName, self.arrayType = get_var(self.code[1])
        self.index = get_expr(code[2], self.env)
        self.env = self.index.env
        self.value = get_expr(code[3], self.env)
        self.env = self.value.env
        debug("Eupdate")

    
    def toRust(self) -> str:
        output = "let mut tmp = " + self.arrayName + ".clone();\ntmp[(" + self.index.toRust() + ").to_usize_wrapping()]" + " = " + self.value.toRust()
        output += "; tmp" #tmp is a good variable name because it will fall out of scope here
        # compiler is intelligent : if a clone is not necessary it will not do it
        return output

class Eoperator(expr):
    # Representation of an operator, which is some functions (see OPERATOR_CORR)
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        if not self.code[0].strip(' \n') in OPERATOR_CORR.keys():
            raise Exception("E >> can't parse operation : " + self.code)
        self.op = OPERATOR_CORR[code[0]]

        self.leftOp = get_expr(self.code[1], self.env)
        self.env = self.leftOp.env
        self.rightOp = get_expr(self.code[2], self.env)
        self.env = self.rightOp.env

        debug("Eoperator : operator " + self.op)
    
    def toRust(self) -> str:
        return self.leftOp.toRust() + self.op + self.rightOp.toRust()

class Eappication(expr):
    # Representation of an expression, fn name must be is FN_NAMES
    def __init__(self, code, env = []) -> None:
        self.code = code
        self.env = env

        try:
            self.name = code[0].strip(' \n')
        except:
            raise Exception("E >> error while parsing function: " + code)

        debug("Eapplication : application " + self.name)
    
    def toRust(self) -> str:
        output = self.name + "("
        for argCode in self.code[1:]:
            if not isinstance(argCode, str) or argCode.strip(' \n') != 'nil':
                output += get_expr(argCode, self.env).toRust() + ','
        output = output.strip(',') + ")"
        return output

class Efn(expr):
    # Representation of a function, it updates the env and returns a 
    # boxed (std::Box) closure, except on first level
    def __init__(self, code, env = [], name="") -> None:
        self.code = code
        self.name = name
        self.type = ""
        self.firstLevel = name != ""

        self.args = [] # [[name, type]]
        self.outtype = ""
        self.body = None
        self.env = env 

        self.parse()
        for var in self.env: # mark all variables used (later we need to clone them )
            var[3] = True

        for arg in self.args:
            self.env.append([[arg[0]], arg[0], arg[1], False])
        
        debug("Efn : function " + str(self.args) + " -> " + str(self.outtype))

    def isFn(arr) -> bool:
        try:
            assert(arr[0].strip(' \n') == 'lambda')
            assert(not isinstance(arr[1], str))
            assert(arr[2].strip(' \n') == "'->")
            return True
        except:
            return False

    def parse(self):
        try:
            assert(Efn.isFn(self.code))
            for var in self.code[1]:
                v, t = get_var(var)
                self.args.append([v.strip(' \n'), t.strip(' \n')])
            self.outtype = get_type(self.code[3])
            self.body = self.code[4]

            self.type = "Box<impl Fn(" 
            for arg in self.args:
                self.type += arg[1] + ','
            self.type = self.type.strip(',') + ") -> " + self.outtype + '>'

        except:
            raise Exception("E >> can't parse fn : " + str(self.code))
        
    def toRust(self):
        if self.firstLevel: #we are at the base level
            output = "fn " + self.name + "("
            for arg in self.args:
                output += arg[0] + ": " + arg[1] + ","
            output = output.strip(',') + ") -> " + self.outtype + '{'
            output += get_expr(self.body, self.env).toRust() + '}'
        else:
            output = "Box::new(move |"
            for arg in self.args:
                output += arg[0] + ": " + arg[1] + ","
            output = output.strip(',') + "| -> " + self.outtype + '{'
            output += get_expr(self.body, self.env).toRust() + '})'
        return output
