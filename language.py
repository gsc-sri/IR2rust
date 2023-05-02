from language_types import *

DEBUG = True

def debug(c: str) -> None:
    if DEBUG:
        print("DEBUG >> " + c)


OPERATOR_CORR = {"+": "+",
                 "-": "-",
                 "*": "*",
                 "/": "/",
                 "nrem": "%",
                 "=": "==",
                 "<": "<"
                 }

CONSTS = ['true', 'false'] # we may add user-declared consts in Evalue


class expr:
    # abstract class for expressions (= everything)
    # the init must parse
    def __init__(self, code : str | list , env=[]) -> None:
        self.code: str = None
        self.env: list[var] = None
        self.usedVars: list[var] = None
        raise Exception("Must implement __init__ function !")

    def toRust(self) -> str:
        raise Exception("Must implement toRust function !")


class var:
    # Represents a variable of the env
    def __init__(self, name: str, type: str, scope: expr, isArg = False) -> None:
        self.name: str = name
        self.names: list[str] = [name]
        self.type: str = type
        self.used: bool = False
        self.scope: expr = scope # Not used rn but may be for better memory management
        self.mutable: bool = False
        self.isArg: bool = isArg

    def __str__(self) -> str:
        return "VAR " + self.name + " arg " + str(self.isArg) + " mut " + str(self.mutable)


class env:
    # The set of currently used variable
    def __init__(self, from_env=None):
        self.variables: list[var] = [] if from_env == None else from_env.variables

    def get_var(self, s: str):
        s = s.strip(' \n')
        for var in self.variables:
            if s in var.names:
                return var
        debug("WARN : var " + s + " not found in env " + str(self))
        return None

    def set_used(self, s: str):
        self.get_var(s).used = True

    def __str__(self) -> str:
        output = ""
        for var in self.variables:
            output += str(var) + "\n"
        return output


def get_expr(tabl: list[list | str] | str, env: env, name = "") -> expr:
    # From ['object', ...] to corresponding expr
    if isinstance(tabl, str): # int bool etc
        return Evalue(tabl, env, name)
    try:
        key = tabl[0]
        if not isinstance(key, str):  # handles cases such as [[ thing ]]
            if len(tabl) < 2:
                return get_expr(key, env)
            else:
                # lambda calls : [[expr fn] [expr arg]]
                return Elambdacall(tabl, env)
        else:
            key = key.strip(' \n')  # hence str
    except:
        raise Exception("E >> error getting expr from : " + str(tabl))

    if key == "lambda": return Efn(tabl, env, name)
    elif key == "let": return Elet(tabl, env)
    elif key == "if": return Eif(tabl, env)
    elif key == "release": return Erelease(tabl, env)
    elif key == "lett": return Elett(tabl, env)
    elif key == "lookup": return Elookup(tabl, env)
    elif key == "get": return Eget(tabl, env)
    elif key == "update": 
        if isArray(tabl[1]):
            return Eupdate_array(tabl, env)
        elif isRecordtype(tabl[1]):
            return Eupdate_recordtype(tabl, env)
        raise Exception("E >> cannot find right update expr for : " + str(tabl[1]))
    elif key in OPERATOR_CORR.keys(): return Eoperator(tabl, env)
    elif key[:4] == "ivar" or key == "last": return Evariable(tabl, env)
    else: return Eappication(tabl, env)


class Evariable(expr):
    # Representation of a variable with possibly a last before
    # Here is a representation for variables as expr ! Hence they
    # must already be in the env. For declaration see Elet and Efn
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        if not Evariable.isVariable(self.code):
            raise Exception("E >> can't parse variable : " + self.code)

        self.isLast = code[0].strip(' \n') == 'last'
        if self.isLast:
            self.code = self.code[1]

        self.name = self.code[0].strip(' \n')

        self.fromEnv = self.env.get_var(self.name)

        if self.fromEnv == None:
            raise Exception("E >> can't find variable " +
                            self.name + " in env " + str(self.env.variables))
        
        self.usedVars: list[var] = [self.fromEnv]

        self.name = self.fromEnv.name
        self.type = self.fromEnv.type
        self.used = self.fromEnv.used

        debug("Evariable : Fetched var " + self.name + " of type " +
              self.type + " from env, used : " + str(self.used))

    def isVariable(arr) -> bool:
        try:
            if arr[0].strip(" \n") == "last":
                return Evariable.isVariable(arr[1])
            return True
        except:
            return False

    def toRust(self) -> str:
        output = self.name
        if self.used and not self.isLast: 
            output += ".clone()"
        return output


class Evalue(expr):
    # Representation of a value sur as "123"
    def __init__(self, code: str, env: env, name = "") -> None:
        self.code = code.strip(' \n')
        self.env = env
        self.usedVars: list[var] = []
        self.name = name.strip(' \n')
        global CONSTS

        if not Evalue.isValue(self.code) and not self.code in CONSTS:
            raise Exception("E >> can't parse value : " + self.code)

        if self.name != "": # we are declaring a const
            if self.code.isdigit():
                self.code = "const " + self.name + " : i32 = " + self.code + ";"
            else:
                self.code = "static " + self.name + " : &str = '" + self.code + "';"
            CONSTS.append(self.name)
            debug("Evalue : declaring const : " + self.code)
        else:
            debug("Evalue : returning value " + code)

    def isValue(arr) -> bool:
        return arr.isdigit()

    def toRust(self) -> str:
        return self.code


class Elambdacall(expr):
    # Representation of a lambda call: the first element is a var
    # containing a fn, the following are the arguments
    # TODO :
    #   Do some more checks
    #   Handles > 1 args
    #   Check that this fn does actually work
    def __init__(self, code: str, env: env) -> None:

        self.code = code
        self.env = env

        self.fn = get_expr(self.code[0], self.env) # type 

        self.body = get_expr(self.code[1], self.env)
        self.env = self.body.env

        self.usedVars: list[var] = self.fn.usedVars + self.body.usedVars

        debug("Elambdacall : calling lamda fn with arg: " + str(code[1]))

    def toRust(self) -> str:
        return self.fn.toRust() + "(" + self.body.toRust()+")"


class Elet(expr):
    # les variables modifiees dans value ne doivent pas etre utilisees plus tard
    # sinon faut copier TODO : mettre un check pour ça
    # Representation of a let. It changes the env with the new variable
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env: env = env

        self.varName: str = self.code[1].strip(' \n')
        self.varType: str = get_type(self.code[2])

        if isinstance(code[3], str) and code[3].strip(' \n') == 'nil':
            raise Exception("E >> trying to assign null value")
            # self.middle cannot be nil (we shall modify the pvs2ir code in that objective)

        self.middle = get_expr(self.code[3], self.env)
        self.env = self.middle.env
        self.env.variables.append(var(self.varName, self.varType, self))
        self.right = get_expr(self.code[4], self.env)

        self.usedVars: list[var] = self.right.usedVars
        self.usedVars += self.middle.usedVars

        debug("Elet : created let for variable " + self.varName)

    def toRust(self) -> str:
        v = self.env.get_var(self.varName)
        if v.mutable:
            output = "{let mut "
        else:
            output = "{let "
        output += v.name + " : " + v.type
        output += " = {" + self.middle.toRust()
        output += '};\n'
        output += self.right.toRust() + "}"
        return output


class Elett(expr):
    # Representation of a lett. It adds a new name for the variable in the env
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        self.varName = self.code[1].strip(' \n')
        self.varType = get_type(self.code[2])

        self.targetVar = get_expr(self.code[4], self.env)
        self.env = self.targetVar.env


        for var in self.env.variables:
            if self.targetVar.name in var.names:
                var.names.append(self.varName)
                break

        self.body: expr = get_expr(self.code[5], self.env)
        self.env = self.body.env
        self.usedVars: list[var] = self.body.usedVars

        debug("Elett : added name " + self.varName + " to var " + self.targetVar)

    def toRust(self) -> str:
        return self.body.toRust()


class Eif(expr):
    # Representation of a if then else
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        self.cond: expr = get_expr(self.code[1], self.env)
        self.env = self.cond.env
        self.true: expr = get_expr(self.code[2], self.env)
        self.env = self.true.env  # conservative
        self.false: expr = get_expr(self.code[3], self.env)
        self.env = self.false.env

        self.usedVars: list[var] = self.cond.usedVars + self.true.usedVars + self.false.usedVars

        debug("Eif : if stmt")

    def toRust(self) -> str:
        output = "if " + self.cond.toRust()
        output += "{" + self.true.toRust()
        output += "} else {" + self.false.toRust() + "}"
        return output


class Erelease(expr):
    # Representation of release
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env
        self.usedVars: list[var] = []
        debug("Erelease : ignoring")

    def toRust(self) -> str:
        return get_expr(self.code[3], self.env).toRust()


class Elookup(expr):
    # Lookup of an array
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        self.var: expr = get_expr(self.code[1], self.env)
        self.env = self.var.env

        self.index: expr = get_expr(self.code[2], self.env)
        self.env = self.index.env

        self.usedVars: list[var] = self.var.usedVars + self.index.usedVars

        debug("Elookup")

    def toRust(self) -> str:
        # the clone is only of ref so not a big deal
        return self.var.toRust() + "[" + self.index.toRust() + " as usize].clone()"
    
    def lhsToRust(self):
        # (*Rc::make_mut(&mut array))[index]
        # Prints the lookup when on the left hand side of an update
        if isinstance(self.var, Evariable):
            return "(*Rc::make_mut(&mut "+ self.var.toRust() +" ))["+ self.index.toRust() +" as usize]"
        elif isinstance(self.var, Elookup):
            return "(*Rc::make_mut(&mut "+ self.var.lhsToRust() +" ))["+ self.index.toRust() +" as usize]"
        else:
            raise Exception("E >> Left hand side array is neither lookup or variable")

class Eget(expr):
    def __init__(self, code: str | list, env=[]) -> None:
        self.code = code
        self.env = env

        self.recordtype : expr = get_expr(self.code[1], self.env)
        self.index : str = code[2].strip(" \n")

        self.usedVars: list[var] = self.recordtype.usedVars 

        debug("Eget : " + self.recordtype.toRust())

    def toRust(self) -> str:
        return self.recordtype.toRust() + "." + self.index + ".clone()"

class Eupdate_array(expr):
    # Update of an array
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        self.array: expr = get_expr(self.code[1], self.env)

        self.env.get_var(Eupdate_array.get_array_name(self.array)).mutable = True

        self.index: expr = get_expr(code[2], self.env)
        self.env = self.index.env
        self.value: expr = get_expr(code[3], self.env)
        self.env = self.value.env

        self.usedVars: list[var] = self.array.usedVars + self.index.usedVars + self.value.usedVars

        debug("Eupdate : array " + self.array.toRust())

    def get_array_name(e : expr):
        if isinstance(e, Evariable):
            return e.fromEnv.name
        elif isinstance(e, Elookup):
            return Eupdate_array.get_array_name(e.var)
        else:
            raise Exception("E >> lookup var is neither Evariable or Elookup")

    def toRust(self) -> str:
        if isinstance(self.array, Elookup):
            output = "(*Rc::make_mut(&mut " + self.array.lhsToRust() + "))["+ self.index.toRust() +" as usize] = "
        else:
            output = "(*Rc::make_mut(&mut " + self.array.toRust() + "))["+ self.index.toRust() +" as usize] = "
        output += self.value.toRust() +"; " + Eupdate_array.get_array_name(self.array)  # no clone : A normal forn
        return output
    
class Eupdate_recordtype(expr):
    def __init__(self, code: str | list, env=[]) -> None:
        self.code = code
        self.env = env

        self.recordtype : expr = get_expr(self.code[1], self.env)
        self.env.get_var(Eupdate_recordtype.get_recordtype_name(self.recordtype)).mutable = True

        self.index : str = code[2].strip(" \n")
        self.value : expr = get_expr(code[3], self.env)
        self.env = self.value.env


        self.usedVars: list[var] = self.recordtype.usedVars + self.value.usedVars

        debug("Eupdate : recordtype " + self.recordtype.toRust())

    def get_recordtype_name(e : expr):
        if isinstance(e, Evariable):
            return e.fromEnv.name
        elif isinstance(e, Eget):
            return Eupdate_recordtype.get_recordtype_name(e.var)
        else:
            raise Exception("E >> get var is neither Evariable or Eget")

    def toRust(self) -> str:
        output = self.recordtype.toRust() + "." + self.index + " = " + self.value.toRust() 
        output += "; " + self.recordtype.toRust()
        return output

class Eoperator(expr):
    # Representation of an operator, which is some functions (see OPERATOR_CORR)
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        if not self.code[0].strip(' \n') in OPERATOR_CORR.keys():
            raise Exception("E >> can't parse operation : " + self.code)
        self.op = OPERATOR_CORR[code[0].strip(' \n')]

        self.leftOp = get_expr(self.code[1], self.env)
        self.env = self.leftOp.env
        self.rightOp = get_expr(self.code[2], self.env)
        self.env = self.rightOp.env

        self.usedVars: list[var] = self.leftOp.usedVars + self.rightOp.usedVars

        debug("Eoperator : operator " + self.op)

    def toRust(self) -> str:
        return self.leftOp.toRust() + self.op + self.rightOp.toRust()


class Eappication(expr):
    # Representation of an expression, fn name must be is FN_NAMES
    # The variables must be cloned if they are used later because the
    # fn will take them in its scope (welcome to rust)
    def __init__(self, code: str, env: env) -> None:
        self.code = code
        self.env = env

        try:
            self.name = code[0].strip(' \n')
        except:
            raise Exception("E >> error while parsing function: " + code)

        self.args: list[Evariable] = []
        for argCode in self.code[1:]:
            if not isinstance(argCode, str) or argCode.strip(' \n') != 'nil':
                self.args.append(get_expr(argCode, self.env))
                self.env = self.args[-1].env

        self.usedVars: list[var] = [arg.usedVars for arg in self.args]

        debug("Eapplication : application " + self.name)

    def toRust(self) -> str:
        output = self.name + "("
        for arg in self.args:
            if arg.isLast:
                output += arg.toRust() + ','
            else:
                output += arg.toRust() + '.clone() ,'
        output = output.strip(',') + ")"
        return output


class Efn(expr):
    # Representation of a function, it updates the env and returns a
    # boxed (std::Box) closure, except on first level
    def __init__(self, code: str, env: env, name="") -> None:
        self.code = code
        self.name = name
        self.type = ""
        self.firstLevel = name != ""

        self.args = []  # [[name, type]]
        self.outtype = ""
        self.body = None
        self.env = env

        self.parse()
        # mark all variables used (later we need to clone them )
        for vari in self.env.variables:
            vari.used = True

        for arg in self.args:
            self.env.variables.append(var(arg[0], arg[1], self, True))

        self.body: expr = get_expr(self.body, self.env)
        self.env = self.body.env

        self.usedVars: list[var] = self.body.usedVars

        debug("Efn : function " + str(self.args) + " -> " + str(self.outtype))
        debug(str(self.env))

    def isFn(arr) -> bool:
        try:
            assert (arr[0].strip(' \n') == 'lambda')
            assert (not isinstance(arr[1], str))
            assert (arr[2].strip(' \n') == "'->")
            return True
        except:
            return False

    def parse(self):
        #try:
        assert (Efn.isFn(self.code))
        for var in self.code[1]:
            v = var[0]
            t = get_type(var[1])
            self.args.append([v.strip(' \n'), t.strip(' \n')])
        self.outtype = get_type(self.code[3])
        self.body = self.code[4]

        self.type = "Box<impl Fn("
        for arg in self.args:
            self.type += arg[1] + ','
        self.type = self.type.strip(',') + ") -> " + self.outtype + '>'
        #except:
        #    raise Exception("E >> can't parse fn : " + str(self.code))

    def toRust(self):
        if self.firstLevel:  # we are at the base level
            output = "fn " + self.name + "("
            for arg in self.args:
                if self.env.get_var(arg[0]).mutable: output += "mut "
                output += arg[0] + ": " + arg[1] + ","
            output = output.strip(',') + ") -> " + self.outtype + '{'
            output += self.body.toRust() + '}'
        else:
            output = "Box::new(move |"
            for arg in self.args:
                if self.env.get_var(arg[0]).mutable: output += "mut "
                output += arg[0] + ": " + arg[1] + ","
            output = output.strip(',') + "| -> " + self.outtype + '{'
            output += self.body.toRust() + '})'
        return output
