
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
    mut ivar_1: [[Integer; 99]; 99],
    ivar_2: Integer,
    ivar_3: Integer
) -> [[Integer; 99]; 99] {
    let ivar_4: bool = { ivar_3 == Integer::from(99) };
    if ivar_4 {
        ivar_1
    } else {
        let ivar_9: [[Integer; 99]; 99] = {
            let ivar_11: Integer = {
                let ivar_16: [Integer; 99] = { ivar_1[ivar_3.to_usize_wrapping()].clone() };
                ivar_16[ivar_2.to_usize_wrapping()].clone()
            };
            let ivar_12: Integer = {
                let ivar_27: [Integer; 99] = { ivar_1[ivar_2.to_usize_wrapping()].clone() };
                ivar_27[ivar_3.to_usize_wrapping()].clone()
            };
            let mut ivar_47: [[Integer; 99]; 99] = {
                let mut ivar_36: [Integer; 99] = { ivar_1[ivar_2.to_usize_wrapping()].clone() };
                let mut ivar_44: [[Integer; 99]; 99] = { ivar_1 };
                let ivar_45: [Integer; 99] = {
                    ivar_36[ivar_3.to_usize_wrapping()] = ivar_11;
                    ivar_36
                };
                ivar_44[ivar_2.to_usize_wrapping()] = ivar_45;
                ivar_44
            };
            let mut ivar_48: [Integer; 99] = { ivar_47[ivar_3.to_usize_wrapping()].clone() };
            let mut ivar_56: [[Integer; 99]; 99] = { ivar_47 };
            let ivar_57: [Integer; 99] = {
                ivar_48[ivar_2.to_usize_wrapping()] = ivar_12;
                ivar_48
            };
            ivar_56[ivar_3.to_usize_wrapping()] = ivar_57;
            ivar_56
        };
        let ivar_72: Integer = { ivar_3 + Integer::from(1) };
        smalltranspose__transpose_step(ivar_9, ivar_2, ivar_72)
    }
}