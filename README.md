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

#### Basic with integers and cloning

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

#### With i32 and Rc

Arrays are now in the heap which is far better
With 100x100 :
```
real    0m0.094s
user    0m0.005s
sys     0m0.001s
```
-> Very good (the most important being user time)

With 1000x1000:
```
real    0m16.339s
user    0m16.027s
sys     0m0.043s
```

#### Taking advantage of update only pre-cloned arrays in IR 

We also removed some superfluous clones.

We may check that's always the case.

With 1000x1000:
```
real    0m0.383s
user    0m0.162s
sys     0m0.004s
```

#### Native transposition

```
real    0m0.231s
user    0m0.010s
sys     0m0.004s
```
Still far better

#### Misc

 compile code:
 ```bash=
 cargo rustc --bin rust-project --profile perf -- -C link-args=-Wl,-stack_size,0x1000000000
 ```

 The allocation during the test takes very little time. 
