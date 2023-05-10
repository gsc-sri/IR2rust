PoC of IR to rust transpilation.
===

## Usage

You need prettier with rust plugin, python >= 3.8
The input is the generated IR, with modifications (see example). The modified PVS
can be found here : https://github.com/gsc-sri/PVS , the pvs2rust.lisp file should be manually loaded prior any call to pvs2rust. 

## First version

Supports:
 - `let`, `lett`, `if`, `release`
 - Integers
 - Arrays : `lookup` & `update` in an optimized way
 - Lambda functions : `lambda`
 - Enums
 - Recordtypes
 - Datatypes (no reduce function)

 To be implemented:
 - Uninterpreted types (going with generic types)

## TODO
Split files
Implement uninterpreted types
Handle subterm, << and reduce functions of datatypes