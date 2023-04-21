
/// IR SRC :

///smalltranspose__test_transpose
///(let ivar_1
///  (-> (subrange 0 99 nil nil)
///   (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)))
///  (lambda ((ivar_5 (subrange 0 99 nil nil) nil))
///    '->
///    (smalltranspose__nat32 : (subrange 0 4294967295 nil nil))
///    (smalltranspose__mkRow (last (ivar_5 (subrange 0 99 nil nil) nil))
///     (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)))
///    nil)
///  (let ivar_18
///    (-> (subrange 0 99 nil nil)
///     (-> (subrange 0 99 nil nil)
///      (smalltranspose__nat32 : (subrange 0 4294967295 nil nil))))
///    (lambda ((ivar_8 (subrange 0 99 nil nil) i))
///      '->
///      (-> (subrange 0 99 nil nil)
///       (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)))
///      (ivar_1
///       (-> (subrange 0 99 nil nil)
///        (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)))
///       Z)
///      ((ivar_1
///        (-> (subrange 0 99 nil nil)
///         (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)))
///        Z)))
///    (lett ivar_15
///     (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil))[99/99]))[99/99]))
///     (-> (subrange 0 99 nil nil)
///      (-> (subrange 0 99 nil nil)
///       (smalltranspose__nat32 : (subrange 0 4294967295 nil nil))))
///     (last (ivar_18
///            (-> (subrange 0 99 nil nil)
///             (-> (subrange 0 99 nil nil)
///              (smalltranspose__nat32 : (subrange 0 4294967295 nil nil))))
///            nil))
///     (let ivar_16
///       (subrange 0 100 nil nil)
///       0
///       (smalltranspose__transpose
///        (last (ivar_15
///               (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil))[99/99]))[99/99]))
///               nil))
///        (last (ivar_16 (subrange 0 100 nil nil) nil)) nil))))

/// OUTPUT:
#[allow(non_snake_case, dead_code)]
fn smalltranspose__transpose_step(
    ivar_1: [[Integer; SIZE]; SIZE],
    ivar_2: Integer,
    ivar_3: Integer
) -> [[Integer; SIZE]; SIZE] {
    let ivar_4: bool = { ivar_3.clone() == Integer::from(SIZE) };
    if ivar_4.clone() {
        ivar_1
    } else {
        let ivar_9: [[Integer; SIZE]; SIZE] = {
            let ivar_11: Integer = {
                let ivar_16: [Integer; SIZE] = { ivar_1[ivar_3.clone().to_usize_wrapping()].clone() };
                ivar_16[ivar_2.clone().to_usize_wrapping()].clone()
            };
            let ivar_12: Integer = {
                let ivar_27: [Integer; SIZE] = { ivar_1[ivar_2.clone().to_usize_wrapping()].clone() };
                ivar_27[ivar_3.clone().to_usize_wrapping()].clone()
            };
            let ivar_47: [[Integer; SIZE]; SIZE] = {
                let ivar_36: [Integer; SIZE] = { ivar_1[ivar_2.clone().to_usize_wrapping()].clone() };
                let ivar_44: [[Integer; SIZE]; SIZE] = { ivar_1 };
                let ivar_45: [Integer; SIZE] = {
                    let mut tmp = ivar_36.clone();
                    tmp[ivar_3.clone().to_usize_wrapping()] = ivar_11;
                    tmp
                };
                let mut tmp = ivar_44.clone();
                tmp[ivar_2.clone().to_usize_wrapping()] = ivar_45;
                tmp
            };
            let ivar_48: [Integer; SIZE] = { ivar_47[ivar_3.clone().to_usize_wrapping()].clone() };
            let ivar_56: [[Integer; SIZE]; SIZE] = { ivar_47 };
            let ivar_57: [Integer; SIZE] = {
                let mut tmp = ivar_48.clone();
                tmp[ivar_2.clone().to_usize_wrapping()] = ivar_12;
                tmp
            };
            let mut tmp = ivar_56.clone();
            tmp[ivar_3.clone().to_usize_wrapping()] = ivar_57;
            tmp
        };
        let ivar_72: Integer = { ivar_3 + Integer::from(1) };
        smalltranspose__transpose_step(ivar_9, ivar_2, ivar_72)
    }
}