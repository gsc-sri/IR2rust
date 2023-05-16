///PVS:
/// 
///hello : THEORY
///BEGIN
///  appl(f : [nat, nat -> nat])(m : nat) : nat = f(m, m+1) 
///END hello

///IR : 
/// 
///hello__appl
///@(lambda ((ivar_1
///           (->
///            (recordtype
///             ((=> (project_1 project_139921) (subrange 0 * nil nil))
///              (=> (project_2 project_239922) (subrange 0 * nil nil))))
///            (subrange 0 * nil nil))
///           f))
///   '->
///   (-> (subrange 0 * nil nil) (subrange 0 * nil nil))
///   (lambda ((ivar_4 (subrange 0 * nil nil) m))
///     '->
///     (subrange 0 * nil nil)
///     (let ivar_14
///       (subrange 0 * nil nil)
///       (+ (ivar_4 (subrange 0 * nil nil) m) 1 (subrange 1 * nil nil))
///       (let ivar_15
///         (recordtype
///          ((=> (project_1 project_139923) (subrange 0 * nil nil))
///           (=> (project_2 project_239924) (subrange 0 * nil nil))))
///         (record
///          (recordtype
///           ((=> (project_1 project_139923) (subrange 0 * nil nil))
///            (=> (project_2 project_239924) (subrange 0 * nil nil))))
///          ((= project_1 (last (ivar_4 (subrange 0 * nil nil) m)))
///           (= project_2 (last (ivar_14 (subrange 0 * nil nil) nil)))))
///         ((ivar_1
///           (->
///            (recordtype
///             ((=> (project_1 project_139921) (subrange 0 * nil nil))
///              (=> (project_2 project_239922) (subrange 0 * nil nil))))
///            (subrange 0 * nil nil))
///           f)
///          (last (ivar_15
///                 (recordtype
///                  ((=> (project_1 project_139923)
///                    (subrange 0 * nil nil))
///                   (=> (project_2 project_239924)
///                    (subrange 0 * nil nil))))
///                 nil))
///          nil)))
///     ((ivar_1
///       (->
///        (recordtype
///         ((=> (project_1 project_139921) (subrange 0 * nil nil))
///          (=> (project_2 project_239922) (subrange 0 * nil nil))))
///        (subrange 0 * nil nil))
///       f)))
///   nil)


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
#[derive(Clone)]
struct record_0 {
    project_1: i32,
    project_2: i32,
}

fn hello__appl(f: Rc<dyn Fn(record_0) -> i32>) -> Rc<dyn Fn(i32) -> i32> {
    Rc::new(move |m: i32| -> i32 {
        let ivar_14: i32 = { m.clone() + 1 };
        let ivar_15: record_0 = { record_0 { project_1: m, project_2: ivar_14 } };
        f(ivar_15)
    })
}