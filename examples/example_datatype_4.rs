#![allow(
    non_snake_case,
    dead_code,
    non_upper_case_globals,
    non_camel_case_types,
    unused_variables,
    unused_parens,
    unused_imports
)]

use std::rc::Rc;
use std::clone::Clone;
use std::hash::Hash;
use std::collections::HashMap;
use std::any::Any;

fn Rc_unwrap_or_clone<T: Clone>(rc: Rc<T>) -> T {
    Rc::try_unwrap(rc).unwrap_or_else(|rc| (*rc).clone())
}

#[derive(Clone, Debug, PartialEq)]
struct ordstruct_adt__ordstruct_adt {}

#[derive(Clone, PartialEq)]
enum btree {
    leaf(leaf),
    node1(node1),
    node2(node2),
}

#[derive(Clone, PartialEq)]
struct leaf {}

#[derive(Clone, PartialEq)]
struct node1 {
    val: Rc<f32>,
    right: Rc<btree>,
}

#[derive(Clone, PartialEq)]
struct node2 {
    val: Rc<f32>,
    right: Rc<btree>,
    left: Rc<btree>,
}

fn btree__leaf() -> btree {
    btree::leaf(leaf {})
}

fn btree__node1(val: f32, right: btree) -> btree {
    btree::node1(node1 { val: Rc::new(val), right: Rc::new(right) })
}

fn btree__node2(val: f32, right: btree, left: btree) -> btree {
    btree::node2(node2 { val: Rc::new(val), right: Rc::new(right), left: Rc::new(left) })
}

fn sigmatopdown2__leafp(a: btree) -> bool {
    match a {
        btree::leaf(ref leaf) => true,
        btree::node1(ref node1) => false,
        btree::node2(ref node2) => false,
    }
}

fn sigmatopdown2__node1p(a: btree) -> bool {
    match a {
        btree::leaf(ref leaf) => false,
        btree::node1(ref node1) => true,
        btree::node2(ref node2) => false,
    }
}

fn sigmatopdown2__node2p(a: btree) -> bool {
    match a {
        btree::leaf(ref leaf) => false,
        btree::node1(ref node1) => false,
        btree::node2(ref node2) => true,
    }
}

fn btree__val<T>(a: btree) -> T {
    match a {
        btree::node1(ref node1) => unsafe {
            std::mem::transmute_copy(&Rc_unwrap_or_clone(node1.val.clone()))
        }
        btree::node2(ref node2) => unsafe {
            std::mem::transmute_copy(&Rc_unwrap_or_clone(node2.val.clone()))
        }
        _ => unreachable!(),
    }
}

fn btree__right<T>(a: btree) -> T {
    match a {
        btree::node1(ref node1) => unsafe {
            std::mem::transmute_copy(&Rc_unwrap_or_clone(node1.right.clone()))
        }
        btree::node2(ref node2) => unsafe {
            std::mem::transmute_copy(&Rc_unwrap_or_clone(node2.right.clone()))
        }
        _ => unreachable!(),
    }
}

fn btree__left<T>(a: btree) -> T {
    match a {
        btree::node2(ref node2) => unsafe {
            std::mem::transmute_copy(&Rc_unwrap_or_clone(node2.left.clone()))
        }
        _ => unreachable!(),
    }
}

fn btree__val__update<T>(a: btree, val: T) -> btree {
    match a {
        btree::node1(ref node1) =>
            btree::node1(node1 {
                val: Rc::new(unsafe { std::mem::transmute_copy(&val) }),
                right: node1.right.clone(),
            }),
        btree::node2(ref node2) =>
            btree::node2(node2 {
                val: Rc::new(unsafe { std::mem::transmute_copy(&val) }),
                right: node2.right.clone(),
                left: node2.left.clone(),
            }),
        _ => unreachable!(),
    }
}

fn btree__right__update<T>(a: btree, right: T) -> btree {
    match a {
        btree::node1(ref node1) =>
            btree::node1(node1 {
                val: node1.val.clone(),
                right: Rc::new(unsafe { std::mem::transmute_copy(&right) }),
            }),
        btree::node2(ref node2) =>
            btree::node2(node2 {
                val: node2.val.clone(),
                right: Rc::new(unsafe { std::mem::transmute_copy(&right) }),
                left: node2.left.clone(),
            }),
        _ => unreachable!(),
    }
}

fn btree__left__update<T>(a: btree, left: T) -> btree {
    match a {
        btree::node2(ref node2) =>
            btree::node2(node2 {
                val: node2.val.clone(),
                right: node2.right.clone(),
                left: Rc::new(unsafe { std::mem::transmute_copy(&left) }),
            }),
        _ => unreachable!(),
    }
}

fn sigmatopdown2__ord(x: btree) -> i32 {
    let ivar_3: bool = { sigmatopdown2__leafp(x.clone()) };
    if ivar_3.clone() {
        0
    } else {
        let ivar_15: bool = { sigmatopdown2__node1p(x.clone()) };
        if ivar_15.clone() {
            1
        } else {
            2
        }
    }
}

fn sigmatopdown2__valeur(a: btree) -> i32 {
    let ivar_3: bool = { sigmatopdown2__leafp(a.clone()) };
    if ivar_3.clone() {
        0
    } else {
        let ivar_15: bool = { sigmatopdown2__node1p(a.clone()) };
        if ivar_15.clone() {
            let ivar_7: i32 = { btree__val(a.clone()) };
            ivar_7
        } else {
            let ivar_19: f32 = { btree__val(a.clone()) };
            ivar_19.floor() as i32
        }
    }
}

fn main() {}