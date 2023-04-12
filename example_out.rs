
/// IR SRC :
/// 
///(lambda ((ivar_1 (subrange 0 * nil nil) n))
///  '->
///  (subrange 0 * nil nil)
///  (let ivar_2
///    boolean
///    (let ivar_4
///      (subrange 2 2 nil nil)
///      2
///      (< (ivar_1 (subrange 0 * nil nil) n)
///         (last (ivar_4 (subrange 2 2 nil nil) nil)) nil))
///    (if (ivar_2 boolean nil)
///        (last (ivar_1 (subrange 0 * nil nil) n))
///      (let ivar_7
///        (subrange 0 * nil nil)
///        (let ivar_15
///          (subrange 0 * nil nil)
///          (let ivar_11
///            (subrange 1 1 nil nil)
///            1
///            (- (ivar_1 (subrange 0 * nil nil) n)
///               (last (ivar_11 (subrange 1 1 nil nil) nil))
///               (rename
///                (((ivar_10 (subrange 0 * nil nil) nil) ivar_1
///                  (subrange 0 * nil nil) n))
///                in (subrange -1 * nil nil))))
///          (is_prime__fibo (last (ivar_15 (subrange 0 * nil nil) nil))
///           nil))
///        (let ivar_8
///          (subrange 0 * nil nil)
///          (let ivar_22
///            (subrange 0 * nil nil)
///            (let ivar_18
///              (subrange 2 2 nil nil)
///              2
///              (- (last (ivar_1 (subrange 0 * nil nil) n))
///                 (last (ivar_18 (subrange 2 2 nil nil) nil))
///                 (rename
///                  (((ivar_17 (subrange 0 * nil nil) nil) ivar_1
///                    (subrange 0 * nil nil) n))
///                  in (subrange -2 * nil nil))))
///            (is_prime__fibo (last (ivar_22 (subrange 0 * nil nil) nil))
///             nil))
///          (+ (last (ivar_7 (subrange 0 * nil nil) nil))
///             (last (ivar_8 (subrange 0 * nil nil) nil))
///             (subrange 0 * nil nil))))))
///  nil)


/// OUTPUT:
use rug::Integer;
fn is_prime__fibo(ivar_1: Integer) -> Integer {
    let ivar_2: bool = {
        let ivar_4: Integer = 2;
        ivar_1 < ivar_4
    };
    if ivar_2 {
        ivar_1
    } else {
        let ivar_7: Integer = {
            let ivar_15: Integer = {
                let ivar_11: Integer = 1;
                ivar_1 - ivar_11
            };
            is_prime__fibo(ivar_15)
        };
        let ivar_8: Integer = {
            let ivar_22: Integer = {
                let ivar_18: Integer = 2;
                ivar_1 - ivar_18
            };
            is_prime__fibo(ivar_22)
        };
        ivar_7 + ivar_8
    }
}