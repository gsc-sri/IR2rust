
/// IR SRC :
////// 
///fibo__f
///(lambda ((ivar_1 (subrange 1 * nil nil) n))
///  '->
///  (-> (subrange 0 * nil nil) (subrange 0 * nil nil))
///  (lambda ((ivar_3 (subrange 0 * nil nil) a))
///    '->
///    (subrange 0 * nil nil)
///    (let ivar_4
///      boolean
///      (< (ivar_3 (subrange 0 * nil nil) a)
///         (ivar_1 (subrange 1 * nil nil) n) nil)
///      (if (ivar_4 boolean nil)
///          (release ((ivar_3 (subrange 0 * nil nil) a)) nil 0)
///        (let ivar_11
///          (subrange 0 * nil nil)
///          (let ivar_20
///            (-> (subrange 0 * nil nil) (subrange 0 * nil nil))
///            (fibo__f (ivar_1 (subrange 1 * nil nil) n) nil)
///            (let ivar_26
///              (subrange 0 * nil nil)
///              (- (last (ivar_3 (subrange 0 * nil nil) a))
///                 (ivar_1 (subrange 1 * nil nil) n)
///                 (rename
///                  (((ivar_14 (subrange 1 * nil nil) nil) ivar_1
///                    (subrange 1 * nil nil) n)
///                   ((ivar_13 (subrange 0 * nil nil) nil) ivar_3
///                    (subrange 0 * nil nil) a))
///                  in (subrange * * nil nil)))
///              ((last (ivar_20
///                      (-> (subrange 0 * nil nil)
///                       (subrange 0 * nil nil))
///                      nil))
///               (last (ivar_26 (subrange 0 * nil nil) nil)) nil)))
///          (+ 1 (last (ivar_11 (subrange 0 * nil nil) nil))
///             (subrange 1 * nil nil)))))
///    ((ivar_1 (subrange 1 * nil nil) n)))
///  nil)

/// OUTPUT:
use rug::Integer;

fn fibo_f(ivar_1: Integer) -> Box<dyn Fn(Integer) -> Integer> {
    Box::new(move |ivar_3: Integer| -> Integer {
        let ivar_4: bool = { ivar_3 < ivar_1.clone() };
        if ivar_4 {
            Integer::from(0)
        } else {
            let ivar_11: Integer = {
                let ivar_20: Box<dyn Fn(Integer) -> Integer> = { fibo_f(ivar_1.clone()) };
                let ivar_26: Integer = { ivar_3 - ivar_1.clone() };
                ivar_20(ivar_26)
            };
            Integer::from(1) + ivar_11
        }
    })
}

/// TEST:
fn main(){
    println!("{}", fibo_f(Integer::from(5))(Integer::from(17)))
}