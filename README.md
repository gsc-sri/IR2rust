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
On 4/21/23, transposition of 99x99 matrix takes 
```
real    0m0.581s
user    0m0.474s
sys     0m0.011s
```
with Rug (i had to increase stack size at compile time, prod build)
With u32 int : 
```
real    0m0.296s
user    0m0.054s
sys     0m0.005s
```
--> It looks like it's not really a metter of interface.
TODO : 
 - test with other big int library for rust
 - compare to C code, we should be able to reach x3 time C code 

 compile code:
 ```bash=
 cargo rustc --bin rust-project --profile perf -- -C link-args=-Wl,-stack_size,0x1000000000
 ```

