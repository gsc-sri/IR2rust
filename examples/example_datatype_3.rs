///PVS :
///
///sigmatopdown2	: THEORY
///
///  BEGIN
///
///btree: DATATYPE
///BEGIN
///  leaf: leaf?
///  pending(a : btree): pending?
///END btree
///
///END sigmatopdown2


///IR : 
/// 
///DATATYPE btree THEORY sigmatopdown2
///@(
///(CONSTRUCTOR leaf)
///(CONSTRUCTOR pending
///(ACCESSOR a (btree : adt-recordtype))))
///$sigmatopdown2__btree_ord
///@(exit)
///
///$sigmatopdown2__ord
///@(lambda ((ivar_1 (btree : adt-recordtype) x))
///   '->
///   (subrange 0 1 nil nil)
///   (let ivar_3
///     bool
///     (sigmatopdown2__leafp (ivar_1 (btree : adt-recordtype) x) nil)
///     (if (ivar_3 bool nil)
///         (release ((ivar_1 (btree : adt-recordtype) x)) nil 0)
///       1))
///   nil)
///
///$sigmatopdown2__subterm
///@(lambda ((ivar_1 (btree : adt-recordtype) x)
///          (ivar_2 (btree : adt-recordtype) y))
///   '->
///   bool
///   (let ivar_3
///     bool
///     (= (ivar_1 (btree : adt-recordtype) x)
///        (ivar_2 (btree : adt-recordtype) y) nil)
///     (if (ivar_3 bool nil)
///         (release
///          ((ivar_1 (btree : adt-recordtype) x)
///           (ivar_2 (btree : adt-recordtype) y))
///          nil true)
///       (let ivar_9
///         bool
///         (sigmatopdown2__leafp (ivar_2 (btree : adt-recordtype) y) nil)
///         (if (ivar_9 bool nil)
///             (release
///              ((ivar_1 (btree : adt-recordtype) x)
///               (ivar_2 (btree : adt-recordtype) y))
///              nil false)
///           (let ivar_13
///             (btree : adt-recordtype)
///             (btree__a (last (ivar_2 (btree : adt-recordtype) y)) nil)
///             (sigmatopdown2__subterm
///              (last (ivar_1 (btree : adt-recordtype) x))
///              (last (ivar_13 (btree : adt-recordtype) nil)) nil))))))
///   nil)
///
///$sigmatopdown2__doublelessp
///@(lambda ((ivar_1 (btree : adt-recordtype) x)
///          (ivar_2 (btree : adt-recordtype) y))
///   '->
///   bool
///   (let ivar_4
///     bool
///     (sigmatopdown2__leafp (ivar_2 (btree : adt-recordtype) y) nil)
///     (if (ivar_4 bool nil)
///         (release
///          ((ivar_1 (btree : adt-recordtype) x)
///           (ivar_2 (btree : adt-recordtype) y))
///          nil false)
///       (let ivar_8
///         (btree : adt-recordtype)
///         (btree__a (last (ivar_2 (btree : adt-recordtype) y)) nil)
///         (let ivar_12
///           bool
///           (= (ivar_1 (btree : adt-recordtype) x)
///              (ivar_8 (btree : adt-recordtype) nil) nil)
///           (if (ivar_12 bool nil)
///               (release
///                ((ivar_8 (btree : adt-recordtype) nil)
///                 (ivar_1 (btree : adt-recordtype) x))
///                nil true)
///             (sigmatopdown2__doublelessp
///              (last (ivar_1 (btree : adt-recordtype) x))
///              (last (ivar_8 (btree : adt-recordtype) nil)) nil))))))
///   nil)
///
///$sigmatopdown2__reduce_nat
///@(lambda ((ivar_1 (subrange 0 * nil nil) leaf?_fun)
///          (ivar_2 (-> (subrange 0 * nil nil) (subrange 0 * nil nil))
///           pending?_fun))
///   '->
///   (-> (btree : adt-recordtype) (subrange 0 * nil nil))
///   (lambda ((ivar_5 (btree : adt-recordtype) btree_adtvar))
///     '->
///     (subrange 0 * nil nil)
///     (let ivar_6
///       (-> (btree : adt-recordtype) (subrange 0 * nil nil))
///       (sigmatopdown2__reduce_nat
///        (ivar_1 (subrange 0 * nil nil) leaf?_fun)
///        (ivar_2 (-> (subrange 0 * nil nil) (subrange 0 * nil nil))
///         pending?_fun)
///        nil)
///       (let ivar_17
///         bool
///         (sigmatopdown2__leafp
///          (ivar_5 (btree : adt-recordtype) btree_adtvar) nil)
///         (if (ivar_17 bool nil)
///             (release
///              ((ivar_6
///                (-> (btree : adt-recordtype) (subrange 0 * nil nil))
///                red)
///               (ivar_5 (btree : adt-recordtype) btree_adtvar))
///              nil (ivar_1 (subrange 0 * nil nil) leaf?_fun))
///           (let ivar_21
///             (btree : adt-recordtype)
///             (btree__a
///              (last (ivar_5 (btree : adt-recordtype) btree_adtvar))
///              nil)
///             (let ivar_34
///               (subrange 0 * nil nil)
///               ((last (ivar_6
///                       (-> (btree : adt-recordtype)
///                        (subrange 0 * nil nil))
///                       red))
///                (last (ivar_21 (btree : adt-recordtype) nil)) nil)
///               ((ivar_2
///                 (-> (subrange 0 * nil nil) (subrange 0 * nil nil))
///                 pending?_fun)
///                (last (ivar_34 (subrange 0 * nil nil) nil)) nil))))))
///     ((ivar_2 (-> (subrange 0 * nil nil) (subrange 0 * nil nil))
///       pending?_fun)
///      (ivar_1 (subrange 0 * nil nil) leaf?_fun)))
///   nil)
///
///$sigmatopdown2__REDUCE_nat
///@(lambda ((ivar_1 (-> (btree : adt-recordtype) (subrange 0 * nil nil))
///           leaf?_fun)
///          (ivar_3
///           (->
///            (recordtype
///             ((=> (project_1 project_140046) (subrange 0 * nil nil))
///              (=> (project_2 project_240047)
///               (btree : adt-recordtype))))
///            (subrange 0 * nil nil))
///           pending?_fun))
///   '->
///   (-> (btree : adt-recordtype) (subrange 0 * nil nil))
///   (lambda ((ivar_6 (btree : adt-recordtype) btree_adtvar))
///     '->
///     (subrange 0 * nil nil)
///     (let ivar_7
///       (-> (btree : adt-recordtype) (subrange 0 * nil nil))
///       (sigmatopdown2__REDUCE_nat
///        (ivar_1 (-> (btree : adt-recordtype) (subrange 0 * nil nil))
///         leaf?_fun)
///        (ivar_3
///         (->
///          (recordtype
///           ((=> (project_1 project_140046) (subrange 0 * nil nil))
///            (=> (project_2 project_240047) (btree : adt-recordtype))))
///          (subrange 0 * nil nil))
///         pending?_fun)
///        nil)
///       (let ivar_24
///         bool
///         (sigmatopdown2__leafp
///          (ivar_6 (btree : adt-recordtype) btree_adtvar) nil)
///         (if (ivar_24 bool nil)
///             (release
///              ((ivar_7
///                (-> (btree : adt-recordtype) (subrange 0 * nil nil))
///                red))
///              nil
///              ((ivar_1
///                (-> (btree : adt-recordtype) (subrange 0 * nil nil))
///                leaf?_fun)
///               (last (ivar_6 (btree : adt-recordtype) btree_adtvar))
///               nil))
///           (let ivar_28
///             (btree : adt-recordtype)
///             (btree__a (ivar_6 (btree : adt-recordtype) btree_adtvar)
///              nil)
///             (let ivar_42
///               (subrange 0 * nil nil)
///               ((last (ivar_7
///                       (-> (btree : adt-recordtype)
///                        (subrange 0 * nil nil))
///                       red))
///                (last (ivar_28 (btree : adt-recordtype) nil)) nil)
///               (let ivar_44
///                 (recordtype
///                  ((=> (project_1 project_140051)
///                    (subrange 0 * nil nil))
///                   (=> (project_2 project_240052)
///                    (btree : adt-recordtype))))
///                 (record
///                  (recordtype
///                   ((=> (project_1 project_140051)
///                     (subrange 0 * nil nil))
///                    (=> (project_2 project_240052)
///                     (btree : adt-recordtype))))
///                  ((= project_1
///                      (last (ivar_42 (subrange 0 * nil nil) nil)))
///                   (= project_2
///                      (last (ivar_6 (btree : adt-recordtype)
///                             btree_adtvar)))))
///                 ((ivar_3
///                   (->
///                    (recordtype
///                     ((=> (project_1 project_140046)
///                       (subrange 0 * nil nil))
///                      (=> (project_2 project_240047)
///                       (btree : adt-recordtype))))
///                    (subrange 0 * nil nil))
///                   pending?_fun)
///                  (last (ivar_44
///                         (recordtype
///                          ((=> (project_1 project_140051)
///                            (subrange 0 * nil nil))
///                           (=> (project_2 project_240052)
///                            (btree : adt-recordtype))))
///                         nil))
///                  nil)))))))
///     ((ivar_3
///       (->
///        (recordtype
///         ((=> (project_1 project_140046) (subrange 0 * nil nil))
///          (=> (project_2 project_240047) (btree : adt-recordtype))))
///        (subrange 0 * nil nil))
///       pending?_fun)
///      (ivar_1 (-> (btree : adt-recordtype) (subrange 0 * nil nil))
///       leaf?_fun)))
///   nil)
///
///$sigmatopdown2__reduce_ordinal
///@(lambda ((ivar_1 (ordstruct_adt__ordstruct_adt : adt-recordtype)
///           leaf?_fun)
///          (ivar_2
///           (-> (ordstruct_adt__ordstruct_adt : adt-recordtype)
///            (ordstruct_adt__ordstruct_adt : adt-recordtype))
///           pending?_fun))
///   '->
///   (-> (btree : adt-recordtype)
///    (ordstruct_adt__ordstruct_adt : adt-recordtype))
///   (lambda ((ivar_5 (btree : adt-recordtype) btree_adtvar))
///     '->
///     (ordstruct_adt__ordstruct_adt : adt-recordtype)
///     (let ivar_6
///       (-> (btree : adt-recordtype)
///        (ordstruct_adt__ordstruct_adt : adt-recordtype))
///       (sigmatopdown2__reduce_ordinal
///        (ivar_1 (ordstruct_adt__ordstruct_adt : adt-recordtype)
///         leaf?_fun)
///        (ivar_2
///         (-> (ordstruct_adt__ordstruct_adt : adt-recordtype)
///          (ordstruct_adt__ordstruct_adt : adt-recordtype))
///         pending?_fun)
///        nil)
///       (let ivar_17
///         bool
///         (sigmatopdown2__leafp
///          (ivar_5 (btree : adt-recordtype) btree_adtvar) nil)
///         (if (ivar_17 bool nil)
///             (release
///              ((ivar_6
///                (-> (btree : adt-recordtype)
///                 (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                red)
///               (ivar_5 (btree : adt-recordtype) btree_adtvar))
///              nil
///              (ivar_1 (ordstruct_adt__ordstruct_adt : adt-recordtype)
///               leaf?_fun))
///           (let ivar_21
///             (btree : adt-recordtype)
///             (btree__a
///              (last (ivar_5 (btree : adt-recordtype) btree_adtvar))
///              nil)
///             (let ivar_34
///               (ordstruct_adt__ordstruct_adt : adt-recordtype)
///               ((last (ivar_6
///                       (-> (btree : adt-recordtype)
///                        (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                       red))
///                (last (ivar_21 (btree : adt-recordtype) nil)) nil)
///               ((ivar_2
///                 (-> (ordstruct_adt__ordstruct_adt : adt-recordtype)
///                  (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                 pending?_fun)
///                (last (ivar_34
///                       (ordstruct_adt__ordstruct_adt : adt-recordtype)
///                       nil))
///                nil))))))
///     ((ivar_2
///       (-> (ordstruct_adt__ordstruct_adt : adt-recordtype)
///        (ordstruct_adt__ordstruct_adt : adt-recordtype))
///       pending?_fun)
///      (ivar_1 (ordstruct_adt__ordstruct_adt : adt-recordtype)
///       leaf?_fun)))
///   nil)
///
///$sigmatopdown2__REDUCE_ordinal
///@(lambda ((ivar_1
///           (-> (btree : adt-recordtype)
///            (ordstruct_adt__ordstruct_adt : adt-recordtype))
///           leaf?_fun)
///          (ivar_3
///           (->
///            (recordtype
///             ((=> (project_1 project_140205)
///               (ordstruct_adt__ordstruct_adt : adt-recordtype))
///              (=> (project_2 project_240206)
///               (btree : adt-recordtype))))
///            (ordstruct_adt__ordstruct_adt : adt-recordtype))
///           pending?_fun))
///   '->
///   (-> (btree : adt-recordtype)
///    (ordstruct_adt__ordstruct_adt : adt-recordtype))
///   (lambda ((ivar_6 (btree : adt-recordtype) btree_adtvar))
///     '->
///     (ordstruct_adt__ordstruct_adt : adt-recordtype)
///     (let ivar_7
///       (-> (btree : adt-recordtype)
///        (ordstruct_adt__ordstruct_adt : adt-recordtype))
///       (sigmatopdown2__REDUCE_ordinal
///        (ivar_1
///         (-> (btree : adt-recordtype)
///          (ordstruct_adt__ordstruct_adt : adt-recordtype))
///         leaf?_fun)
///        (ivar_3
///         (->
///          (recordtype
///           ((=> (project_1 project_140205)
///             (ordstruct_adt__ordstruct_adt : adt-recordtype))
///            (=> (project_2 project_240206) (btree : adt-recordtype))))
///          (ordstruct_adt__ordstruct_adt : adt-recordtype))
///         pending?_fun)
///        nil)
///       (let ivar_24
///         bool
///         (sigmatopdown2__leafp
///          (ivar_6 (btree : adt-recordtype) btree_adtvar) nil)
///         (if (ivar_24 bool nil)
///             (release
///              ((ivar_7
///                (-> (btree : adt-recordtype)
///                 (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                red))
///              nil
///              ((ivar_1
///                (-> (btree : adt-recordtype)
///                 (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                leaf?_fun)
///               (last (ivar_6 (btree : adt-recordtype) btree_adtvar))
///               nil))
///           (let ivar_28
///             (btree : adt-recordtype)
///             (btree__a (ivar_6 (btree : adt-recordtype) btree_adtvar)
///              nil)
///             (let ivar_42
///               (ordstruct_adt__ordstruct_adt : adt-recordtype)
///               ((last (ivar_7
///                       (-> (btree : adt-recordtype)
///                        (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                       red))
///                (last (ivar_28 (btree : adt-recordtype) nil)) nil)
///               (let ivar_44
///                 (recordtype
///                  ((=> (project_1 project_140210)
///                    (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                   (=> (project_2 project_240211)
///                    (btree : adt-recordtype))))
///                 (record
///                  (recordtype
///                   ((=> (project_1 project_140210)
///                     (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                    (=> (project_2 project_240211)
///                     (btree : adt-recordtype))))
///                  ((= project_1
///                      (last (ivar_42
///                             (ordstruct_adt__ordstruct_adt : adt-recordtype)
///                             nil)))
///                   (= project_2
///                      (last (ivar_6 (btree : adt-recordtype)
///                             btree_adtvar)))))
///                 ((ivar_3
///                   (->
///                    (recordtype
///                     ((=> (project_1 project_140205)
///                       (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                      (=> (project_2 project_240206)
///                       (btree : adt-recordtype))))
///                    (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                   pending?_fun)
///                  (last (ivar_44
///                         (recordtype
///                          ((=> (project_1 project_140210)
///                            (ordstruct_adt__ordstruct_adt : adt-recordtype))
///                           (=> (project_2 project_240211)
///                            (btree : adt-recordtype))))
///                         nil))
///                  nil)))))))
///     ((ivar_3
///       (->
///        (recordtype
///         ((=> (project_1 project_140205)
///           (ordstruct_adt__ordstruct_adt : adt-recordtype))
///          (=> (project_2 project_240206) (btree : adt-recordtype))))
///        (ordstruct_adt__ordstruct_adt : adt-recordtype))
///       pending?_fun)
///      (ivar_1
///       (-> (btree : adt-recordtype)
///        (ordstruct_adt__ordstruct_adt : adt-recordtype))
///       leaf?_fun)))
///   nil)

/// Rust :

#![allow(
    non_snake_case,
    dead_code,
    non_upper_case_globals,
    non_camel_case_types,
    unused_variables,
    unused_parens
)]

use std::rc::Rc;
use std::clone::Clone;
use std::any::Any;

fn Rc_unwrap_or_clone<T: Clone>(rc: Rc<T>) -> T {
    Rc::try_unwrap(rc).unwrap_or_else(|rc| (*rc).clone())
}

#[derive(Clone, Debug, PartialEq)]
struct ordstruct_adt__ordstruct_adt {}

#[derive(Clone)]
struct record_0 {
    project_1: i32,
    project_2: btree,
}
#[derive(Clone)]
struct record_1 {
    project_1: ordstruct_adt__ordstruct_adt,
    project_2: btree,
}

trait btree_trait {
    fn sigmatopdown2__leafp(self: Self) -> bool;
    fn btree__leaf() -> btree {
        btree {
            ord: 0,
            data: Rc::new(leaf {}),
        }
    }
    fn sigmatopdown2__pendingp(self: Self) -> bool;
    fn btree__a(self: Self) -> btree;
    fn btree__a__update(self: Self, a: btree) -> btree;
    fn btree__pending(a: btree) -> btree {
        btree {
            ord: 1,
            data: Rc::new(pending { a: a }),
        }
    }
}

#[derive(Clone, Debug)]
struct btree {
    ord: i32,
    data: Rc<dyn Any>,
}
#[derive(Clone, PartialEq, Debug)]
struct leaf {}

#[derive(Clone, PartialEq, Debug)]
struct pending {
    a: btree,
}

impl PartialEq for btree {
    fn eq(&self, other: &Self) -> bool {
        if self.ord == other.ord {
            if self.ord == 0 {
                return (
                    Rc::downcast::<leaf>(self.data.clone()).unwrap() ==
                    Rc::downcast::<leaf>(other.data.clone()).unwrap()
                );
            }
            if self.ord == 1 {
                return (
                    Rc::downcast::<pending>(self.data.clone()).unwrap() ==
                    Rc::downcast::<pending>(other.data.clone()).unwrap()
                );
            }
        }
        false
    }
}

impl btree_trait for btree {
    fn sigmatopdown2__leafp(self: Self) -> bool {
        self.ord == 0
    }
    fn sigmatopdown2__pendingp(self: Self) -> bool {
        self.ord == 1
    }
    fn btree__a(self: Self) -> btree {
        Rc_unwrap_or_clone(Rc::downcast::<pending>(self.data).unwrap()).a
    }
    fn btree__a__update(self: Self, a: btree) -> btree {
        let mut updated = Rc::downcast::<pending>(self.data).unwrap();
        Rc::make_mut(&mut updated).a = a;
        btree { ord: 1, data: updated }
    }
}

exit();

fn sigmatopdown2__ord(x: btree) -> i32 {
    let ivar_3: bool = { x.clone().sigmatopdown2__leafp() };
    if ivar_3.clone() {
        0
    } else {
        1
    }
}

fn sigmatopdown2__subterm(x: btree, y: btree) -> bool {
    let ivar_3: bool = { x.clone() == y.clone() };
    if ivar_3.clone() {
        true
    } else {
        let ivar_9: bool = { y.clone().sigmatopdown2__leafp() };
        if ivar_9.clone() {
            false
        } else {
            let ivar_13: btree = { y.btree__a() };
            sigmatopdown2__subterm(x, ivar_13)
        }
    }
}

fn sigmatopdown2__doublelessp(x: btree, y: btree) -> bool {
    let ivar_4: bool = { y.clone().sigmatopdown2__leafp() };
    if ivar_4.clone() {
        false
    } else {
        let ivar_8: btree = { y.btree__a() };
        let ivar_12: bool = { x.clone() == ivar_8.clone() };
        if ivar_12.clone() {
            true
        } else {
            sigmatopdown2__doublelessp(x, ivar_8)
        }
    }
}

fn sigmatopdown2__reduce_nat(
    leafqm_fun: i32,
    pendingqm_fun: Rc<dyn Fn(i32) -> i32>
) -> Rc<dyn Fn(btree) -> i32> {
    Rc::new(move |btree_adtvar: btree| -> i32 {
        let ivar_6: Rc<dyn Fn(btree) -> i32> = {
            sigmatopdown2__reduce_nat(leafqm_fun.clone(), pendingqm_fun.clone())
        };
        let ivar_17: bool = { btree_adtvar.clone().sigmatopdown2__leafp() };
        if ivar_17.clone() {
            leafqm_fun.clone()
        } else {
            let ivar_21: btree = { btree_adtvar.btree__a() };
            let ivar_34: i32 = { ivar_6(ivar_21) };
            pendingqm_fun(ivar_34)
        }
    })
}

fn sigmatopdown2__REDUCE_nat(
    leafqm_fun: Rc<dyn Fn(btree) -> i32>,
    pendingqm_fun: Rc<dyn Fn(record_0) -> i32>
) -> Rc<dyn Fn(btree) -> i32> {
    Rc::new(move |btree_adtvar: btree| -> i32 {
        let ivar_7: Rc<dyn Fn(btree) -> i32> = {
            sigmatopdown2__REDUCE_nat(leafqm_fun.clone(), pendingqm_fun.clone())
        };
        let ivar_24: bool = { btree_adtvar.clone().sigmatopdown2__leafp() };
        if ivar_24.clone() {
            leafqm_fun(btree_adtvar)
        } else {
            let ivar_28: btree = { btree_adtvar.clone().btree__a() };
            let ivar_42: i32 = { ivar_7(ivar_28) };
            let ivar_44: record_0 = { record_0 { project_1: ivar_42, project_2: btree_adtvar } };
            pendingqm_fun(ivar_44)
        }
    })
}

fn sigmatopdown2__reduce_ordinal(
    leafqm_fun: ordstruct_adt__ordstruct_adt,
    pendingqm_fun: Rc<dyn Fn(ordstruct_adt__ordstruct_adt) -> ordstruct_adt__ordstruct_adt>
) -> Rc<dyn Fn(btree) -> ordstruct_adt__ordstruct_adt> {
    Rc::new(move |btree_adtvar: btree| -> ordstruct_adt__ordstruct_adt {
        let ivar_6: Rc<dyn Fn(btree) -> ordstruct_adt__ordstruct_adt> = {
            sigmatopdown2__reduce_ordinal(leafqm_fun.clone(), pendingqm_fun.clone())
        };
        let ivar_17: bool = { btree_adtvar.clone().sigmatopdown2__leafp() };
        if ivar_17.clone() {
            leafqm_fun.clone()
        } else {
            let ivar_21: btree = { btree_adtvar.btree__a() };
            let ivar_34: ordstruct_adt__ordstruct_adt = { ivar_6(ivar_21) };
            pendingqm_fun(ivar_34)
        }
    })
}

fn sigmatopdown2__REDUCE_ordinal(
    leafqm_fun: Rc<dyn Fn(btree) -> ordstruct_adt__ordstruct_adt>,
    pendingqm_fun: Rc<dyn Fn(record_1) -> ordstruct_adt__ordstruct_adt>
) -> Rc<dyn Fn(btree) -> ordstruct_adt__ordstruct_adt> {
    Rc::new(move |btree_adtvar: btree| -> ordstruct_adt__ordstruct_adt {
        let ivar_7: Rc<dyn Fn(btree) -> ordstruct_adt__ordstruct_adt> = {
            sigmatopdown2__REDUCE_ordinal(leafqm_fun.clone(), pendingqm_fun.clone())
        };
        let ivar_24: bool = { btree_adtvar.clone().sigmatopdown2__leafp() };
        if ivar_24.clone() {
            leafqm_fun(btree_adtvar)
        } else {
            let ivar_28: btree = { btree_adtvar.clone().btree__a() };
            let ivar_42: ordstruct_adt__ordstruct_adt = { ivar_7(ivar_28) };
            let ivar_44: record_1 = { record_1 { project_1: ivar_42, project_2: btree_adtvar } };
            pendingqm_fun(ivar_44)
        }
    })
}