PoC of IR to rust transpilation.
===

## Usage

You need prettier with rust plugin, python >= 3.8
The input is the generated IR, with modifications (see example). The modified PVS
can be found here : https://github.com/gsc-sri/PVS , the pvs2rust.lisp file should be manually loaded prior any call to pvs2rust. 

## First version

Supports:
 - `let`, `lett`, `if`, `release`
 - Integers (only `i32` because casting would result in a big time loss + overflow detection of rust)
 - Reals (using NotNaN wrapper)
 - Arrays : `lookup` & `update` in an optimized way + creation from function (`lett`)
 - Lambda functions : `lambda`
 - Enums
 - Recordtypes
 - Datatypes
 - Funtypes
 - Primitives : 
 ```PVS
   = /= TRUE FALSE IMPLIES => ⇒ <=> ⇔ AND & ∧ OR ∨ NOT ¬ WHEN IFF + - * /
   < <= > >= floor ceiling nrem ndiv even? odd? 
 ```

 To be implemented:
 - Uninterpreted types (going with generic types)

## TODO
### Implement uninterpreted types
Should be quite straitforward with Rust generic type. But check for compatibility with datatypes accessors and update functions, that already use generic types.

### Handle forall & exists
Only for "small" types.

### Handle prelude lists & more primitives


### Handle dependant types

Types like : 
```PVS
a : TYPE = (b : below(10), c : below(b))
```

### Understand why the actual fn representation is so slow compared to arrays

Use flamegraph : 
Some updates are very slow due to copying,
We should also consider another hashing algorithm.

### Misc

Check that all the types have the Clone + PartialEq + Eq + Hash traits.
 - Funtypes : TBD
 - Records : TBD