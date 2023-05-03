PoC of IR to rust transpilation.
===

## Usage

You need prettier with rust plugin, python >= 3.8
The input is the generated IR, with modifications (see example).

## First version

Supports:
 - `let`, `lett`, `if`, `release`
 - Integers
 - Arrays : `lookup` & `update` in an optimized way
 - Lambda functions : `lambda`
 - Enums
 - Recordtypes

 To be implemented:
 - Uninterpreted types (going with generic types)


## TODO:
### Can we use Rust polymorphism for generic type ?
Yes !
Here is an example (but that's not implemented rn bc not really frequent)
```rust
//appl[T: TYPE]: THEORY
// BEGIN
//  f: VAR [T -> T]
//  y: VAR T
//  appl(f)(y): T = f(y)
// END appl

#[allow(non_snake_case, dead_code)]
fn appl__appl<T : 'static>(f : Box<dyn Fn(T) -> T>) -> Box<dyn Fn(T) -> T>{
    // the trait 'static is mandatory due to the use in the closure
    Box::new(move |y : T| -> T {
        f(y)
    })
} 
```

### Handle datatypes

Starting with basic datatypes : 

```PVS
btree : DATATYPE
BEGIN
  leaf : leaf?
  node(val : nat, left : btree, right : btree) : node?
END btree
```

When used inside a theory, each field has:
 - Accessors (`val()`, `left()` and `right()`; IR : `hello__btree_adt_val`)
 - One constructor (`node(v,l,r)`; IR : `(hello__node hello__val hello__left hello__right)`)
 - One recognizer (`leaf?`; IR : `(r_hello__leafp)`)

### Improve horrible perfs : done

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

#### Let collapsing

Around 10s 1000x1000

#### In place modification

10000x10000
```
real    0m1.666s
user    0m1.443s
sys     0m0.142s
```

#### Misc

 compile code:
 ```bash=
 cargo rustc --bin rust-project --profile perf -- -C link-args=-Wl,-stack_size,0x1000000000
 ```
 The allocation during the test takes very little time. 

test 
Dependent tuple: [x : A, y: B(x), C(x, y)], Dependent record: [# a: A, b : B(a),  c : C(a, b) #], Dependent function: [x: A -> B(x)]