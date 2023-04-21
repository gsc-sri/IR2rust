PoC of IR to rust transpilation.
===

## Usage

You need prettier with rust plugin, python >= 3.8
The input is the generated IR, with modifications (see example).

## First version

Supports:
 - `let`, `lett`, `if`, `release`
 - Integers
 - Arrays : `lookup` & `update`
 - Lambda functions : `lambda`


## TODO:
### Can we use Rust polymorphism for generic type ?
TBD

### Handle recordtypes :

```
  (recordtype
      ((=> (project_1 project_192) (subrange 0 * nil nil))
       (=> (project_2 project_293) (subrange 0 * nil nil))))
```
where project_* are projections from tuples

### Improve horrible perfs
Rust does NOT optimize clones , so that will be our job
