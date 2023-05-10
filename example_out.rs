
/// IR SRC :

///DATATYPE btree_adt 
///@(
///(CONSTRUCTOR btree_adt__leaf)
///(CONSTRUCTOR btree_adt__node
///(ACCESSOR btree_adt__val (subrange 0 * nil nil))
///(ACCESSOR btree_adt__left (btree_adt : adt-recordtype))
///(ACCESSOR btree_adt__right (btree_adt : adt-recordtype))))
///$hello__sum
///@(lambda ((ivar_1 (btree_adt : adt-recordtype) a))
///   '->
///   (subrange 0 * nil nil)
///   (let ivar_3
///     bool
///     (btree_adt__leafp (ivar_1 (btree_adt : adt-recordtype) a) nil)
///     (if (ivar_3 bool nil)
///         (release ((ivar_1 (btree_adt : adt-recordtype) a)) nil 0)
///       (let ivar_7
///         (subrange 0 * nil nil)
///         (btree_adt__val (ivar_1 (btree_adt : adt-recordtype) a) nil)
///         (last (ivar_7 (subrange 0 * nil nil) nil)))))
///   nil)

/// OUTPUT:
#![allow(non_snake_case, dead_code, non_upper_case_globals, non_camel_case_types, unused_variables)]

use std::rc::Rc;
use std::clone::Clone;

trait btree_adt {
    fn btree_adt__leafp(self: Rc<Self>) -> bool;
    fn btree_adt__nodep(self: Rc<Self>) -> bool;
    fn btree_adt__val(self: Rc<Self>) -> i32;
    fn btree_adt__left(self: Rc<Self>) -> Rc<dyn btree_adt>;
    fn btree_adt__right(self: Rc<Self>) -> Rc<dyn btree_adt>;
    fn btree_adt__val__update(self: Rc<Self>, btree_adt__val: i32) -> Rc<dyn btree_adt>;
    fn btree_adt__left__update(
        self: Rc<Self>,
        btree_adt__left: Rc<dyn btree_adt>
    ) -> Rc<dyn btree_adt>;
    fn btree_adt__right__update(
        self: Rc<Self>,
        btree_adt__right: Rc<dyn btree_adt>
    ) -> Rc<dyn btree_adt>;
    fn btree_adt__ord(self: Rc<Self>) -> i32;
}

fn btree_adt__subterm(a: Rc<dyn btree_adt>, b: Rc<dyn btree_adt>) -> bool {
    panic!("Subterm is not implemented yet")
}

fn btree_adt__doublelessp(a: Rc<dyn btree_adt>, b: Rc<dyn btree_adt>) -> bool {
    panic!("<< is not implemented yet")
}

fn btree_adt__btree_adt__leaf() -> Rc<btree_adt__leaf> {
    Rc::new(btree_adt__leaf {})
}

fn btree_adt__btree_adt__node(
    btree_adt__val: i32,
    btree_adt__left: Rc<dyn btree_adt>,
    btree_adt__right: Rc<dyn btree_adt>
) -> Rc<btree_adt__node> {
    Rc::new(btree_adt__node {
        btree_adt__val: btree_adt__val,
        btree_adt__left: btree_adt__left,
        btree_adt__right: btree_adt__right,
    })
}

#[derive(Clone)]
struct btree_adt__leaf {}

#[derive(Clone)]
struct btree_adt__node {
    btree_adt__val: i32,
    btree_adt__left: Rc<dyn btree_adt>,
    btree_adt__right: Rc<dyn btree_adt>,
}

impl btree_adt for btree_adt__leaf {
    fn btree_adt__ord(self: Rc<Self>) -> i32 {
        1
    }
    fn btree_adt__leafp(self: Rc<Self>) -> bool {
        true
    }
    fn btree_adt__nodep(self: Rc<Self>) -> bool {
        false
    }
    fn btree_adt__val(self: Rc<Self>) -> i32 {
        panic!()
    }
    fn btree_adt__left(self: Rc<Self>) -> Rc<dyn btree_adt> {
        panic!()
    }
    fn btree_adt__right(self: Rc<Self>) -> Rc<dyn btree_adt> {
        panic!()
    }
    fn btree_adt__val__update(self: Rc<Self>, btree_adt__val: i32) -> Rc<dyn btree_adt> {
        panic!()
    }
    fn btree_adt__left__update(
        self: Rc<Self>,
        btree_adt__left: Rc<dyn btree_adt>
    ) -> Rc<dyn btree_adt> {
        panic!()
    }
    fn btree_adt__right__update(
        self: Rc<Self>,
        btree_adt__right: Rc<dyn btree_adt>
    ) -> Rc<dyn btree_adt> {
        panic!()
    }
}

impl btree_adt for btree_adt__node {
    fn btree_adt__ord(self: Rc<Self>) -> i32 {
        2
    }
    fn btree_adt__leafp(self: Rc<Self>) -> bool {
        false
    }
    fn btree_adt__nodep(self: Rc<Self>) -> bool {
        true
    }
    fn btree_adt__val(self: Rc<Self>) -> i32 {
        self.btree_adt__val
    }
    fn btree_adt__left(self: Rc<Self>) -> Rc<dyn btree_adt> {
        self.btree_adt__left.clone()
    }
    fn btree_adt__right(self: Rc<Self>) -> Rc<dyn btree_adt> {
        self.btree_adt__right.clone()
    }
    fn btree_adt__val__update(self: Rc<Self>, btree_adt__val: i32) -> Rc<dyn btree_adt> {
        let mut updated: Rc<btree_adt__node> = self.clone();
        (*Rc::make_mut(&mut updated)).btree_adt__val = btree_adt__val;
        updated
    }
    fn btree_adt__left__update(
        self: Rc<Self>,
        btree_adt__left: Rc<dyn btree_adt>
    ) -> Rc<dyn btree_adt> {
        let mut updated: Rc<btree_adt__node> = self.clone();
        (*Rc::make_mut(&mut updated)).btree_adt__left = btree_adt__left;
        updated
    }
    fn btree_adt__right__update(
        self: Rc<Self>,
        btree_adt__right: Rc<dyn btree_adt>
    ) -> Rc<dyn btree_adt> {
        let mut updated: Rc<btree_adt__node> = self.clone();
        (*Rc::make_mut(&mut updated)).btree_adt__right = btree_adt__right;
        updated
    }
}

fn hello__sum(a: Rc<dyn btree_adt>) -> i32 {
    let ivar_3: bool = { a.clone().btree_adt__leafp() };
    if ivar_3 {
        0
    } else {
        let ivar_7: i32 = { a.clone().btree_adt__val() };
        ivar_7
    }
}