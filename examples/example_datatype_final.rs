/// PVS
/// 
/// sigmatopdown2	: THEORY
///
///  BEGIN
///
///  btree: DATATYPE
///  BEGIN
///    leaf: leaf?
///    pending(a : btree): pending?
///  END btree
///  
///  END sigmatopdown2

/// IR
/// 
/// $DATATYPE sigmatopdown2 
///@(
///    (CONSTRUCTOR sigmatopdown2__leaf)
///    (CONSTRUCTOR sigmatopdown2__pending
///    (ACCESSOR sigmatopdown2__a (sigmatopdown2 : adt-recordtype))))
///    
///    $sigmatopdown2__ord
///    @(lambda ((ivar_1 (sigmatopdown2 : adt-recordtype) x))
///       '->
///       (subrange 0 1 nil nil)
///       (let ivar_3
///         bool
///         (sigmatopdown2__leafp (ivar_1 (sigmatopdown2 : adt-recordtype) x)
///          nil)
///         (if (ivar_3 bool nil)
///             (release ((ivar_1 (sigmatopdown2 : adt-recordtype) x)) nil 0)
///           1))
///       nil)
///    
///    $sigmatopdown2__subterm
///    @(lambda ((ivar_1 (sigmatopdown2 : adt-recordtype) x)
///              (ivar_2 (sigmatopdown2 : adt-recordtype) y))
///       '->
///       bool
///       (let ivar_3
///         bool
///         (= (ivar_1 (sigmatopdown2 : adt-recordtype) x)
///            (ivar_2 (sigmatopdown2 : adt-recordtype) y) nil)
///         (if (ivar_3 bool nil)
///             (release
///              ((ivar_1 (sigmatopdown2 : adt-recordtype) x)
///               (ivar_2 (sigmatopdown2 : adt-recordtype) y))
///              nil true)
///           (let ivar_9
///             bool
///             (sigmatopdown2__leafp
///              (ivar_2 (sigmatopdown2 : adt-recordtype) y) nil)
///             (if (ivar_9 bool nil)
///                 (release
///                  ((ivar_1 (sigmatopdown2 : adt-recordtype) x)
///                   (ivar_2 (sigmatopdown2 : adt-recordtype) y))
///                  nil false)
///               (let ivar_13
///                 (sigmatopdown2 : adt-recordtype)
///                 (sigmatopdown2__a
///                  (last (ivar_2 (sigmatopdown2 : adt-recordtype) y)) nil)
///                 (sigmatopdown2__subterm
///                  (last (ivar_1 (sigmatopdown2 : adt-recordtype) x))
///                  (last (ivar_13 (sigmatopdown2 : adt-recordtype) nil))
///                  nil))))))
///       nil)
/// 

/// Rust :

#![allow(non_snake_case, dead_code, non_upper_case_globals, non_camel_case_types, unused_variables)]

use std::rc::Rc;
use std::clone::Clone;

fn Rc_unwrap_or_clone<T: Clone>(rc: Rc<T>) -> T {
    Rc::try_unwrap(rc).unwrap_or_else(|rc| (*rc).clone())
}

trait sigmatopdown2_trait {
    fn sigmatopdown2__leafp(self: Self) -> bool;
    fn sigmatopdown2__sigmatopdown2__leaf() -> sigmatopdown2 {
        sigmatopdown2 {
            is__sigmatopdown2__leaf: true,
            is__sigmatopdown2__pending: false,
            sigmatopdown2__a: None,
        }
    }
    fn sigmatopdown2__pendingp(self: Self) -> bool;
    fn sigmatopdown2__a(self: Self) -> sigmatopdown2;
    fn sigmatopdown2__a__update(self: Self, sigmatopdown2__a: sigmatopdown2) -> sigmatopdown2;
    fn sigmatopdown2__sigmatopdown2__pending(sigmatopdown2__a: sigmatopdown2) -> sigmatopdown2 {
        sigmatopdown2 {
            is__sigmatopdown2__leaf: false,
            is__sigmatopdown2__pending: true,
            sigmatopdown2__a: Some(Rc::new(sigmatopdown2__a)),
        }
    }
}

#[derive(Clone, PartialEq, Debug)]
struct sigmatopdown2 {
    is__sigmatopdown2__leaf: bool,
    is__sigmatopdown2__pending: bool,
    sigmatopdown2__a: Option<Rc<sigmatopdown2>>,
}

impl sigmatopdown2_trait for sigmatopdown2 {
    fn sigmatopdown2__leafp(self: Self) -> bool {
        self.is__sigmatopdown2__leaf
    }
    fn sigmatopdown2__pendingp(self: Self) -> bool {
        self.is__sigmatopdown2__pending
    }
    fn sigmatopdown2__a(self: Self) -> sigmatopdown2 {
        Rc_unwrap_or_clone(self.sigmatopdown2__a.unwrap())
    }
    fn sigmatopdown2__a__update(self: Self, sigmatopdown2__a: sigmatopdown2) -> sigmatopdown2 {
        let mut updated = self.clone();
        updated.sigmatopdown2__a = Some(Rc::new(sigmatopdown2__a));
        updated
    }
}

fn sigmatopdown2__ord(x: sigmatopdown2) -> i32 {
    let ivar_3: bool = { x.clone().sigmatopdown2__leafp() };
    if ivar_3 {
        0
    } else {
        1
    }
}

fn sigmatopdown2__subterm(x: sigmatopdown2, y: sigmatopdown2) -> bool {
    let ivar_3: bool = { x == y };
    if ivar_3 {
        true
    } else {
        let ivar_9: bool = { y.clone().sigmatopdown2__leafp() };
        if ivar_9 {
            false
        } else {
            let ivar_13: sigmatopdown2 = { y.sigmatopdown2__a() };
            sigmatopdown2__subterm(x, ivar_13)
        }
    }
}