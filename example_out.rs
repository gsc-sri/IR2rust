
/// IR SRC :

///smalltranspose__transpose_step
///(lambda ((ivar_1
///          (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///          X)
///         (ivar_2 (subrange 0 99 nil nil) i)
///         (ivar_3 (subrange 1 100 nil nil) j))
///  '->
///  (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///  (let ivar_4
///    boolean
///    (= (ivar_3 (subrange 1 100 nil nil) j) 100 nil)
///    (if (ivar_4 boolean nil)
///        (release
///         ((ivar_3 (subrange 1 100 nil nil) j)
///          (ivar_2 (subrange 0 99 nil nil) i))
///         nil
///         (last (ivar_1
///                (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///                X)))
///      (let ivar_9
///        (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///        (let ivar_11
///          (smalltranspose__nat32 : (subrange 0 4294967295 nil nil))
///          (let ivar_16
///            (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99]))
///            (lookup (ivar_1
///                     (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///                     X)
///                    (ivar_3 (subrange 1 100 nil nil) j))
///            (lookup (last (ivar_16
///                           (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99]))
///                           nil))
///                    (ivar_2 (subrange 0 99 nil nil) i)))
///          (let ivar_12
///            (smalltranspose__nat32 : (subrange 0 4294967295 nil nil))
///            (let ivar_27
///              (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99]))
///              (lookup (ivar_1
///                       (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///                       X)
///                      (ivar_2 (subrange 0 99 nil nil) i))
///              (lookup (last (ivar_27
///                             (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99]))
///                             nil))
///                      (ivar_3 (subrange 1 100 nil nil) j)))
///            (let ivar_40
///              (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///              (update
///               (lookup (last (ivar_1
///                              (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///                              X))
///                       ((ivar_2 (subrange 0 99 nil nil) i)))
///               (ivar_3 (subrange 1 100 nil nil) j)
///               (last (ivar_11
///                      (smalltranspose__nat32 : (subrange 0 4294967295 nil nil))
///                      nil)))
///              (update
///               (lookup (last (ivar_40
///                              (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///                              nil))
///                       ((ivar_3 (subrange 1 100 nil nil) j)))
///               (ivar_2 (subrange 0 99 nil nil) i)
///               (last (ivar_12
///                      (smalltranspose__nat32 : (subrange 0 4294967295 nil nil))
///                      nil))))))
///        (let ivar_58
///          (subrange 1 100 nil nil)
///          (+ (last (ivar_3 (subrange 1 100 nil nil) j)) 1
///             (rename
///              (((ivar_51 (subrange 1 100 nil nil) nil) ivar_3
///                (subrange 1 100 nil nil) j)
///               ((ivar_57 (subrange 0 99 nil nil) nil) ivar_2
///                (subrange 0 99 nil nil) i)
///               ((ivar_56
///                 (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///                 nil)
///                ivar_9
///                (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///                Y))
///              in (subrange 2 101 nil nil)))
///          (smalltranspose__transpose_step
///           (last (ivar_9
///                  (smalltranspose__square : (array (smalltranspose__line : (array (smalltranspose__nat32 : (subrange 0 4294967295 nil nil)) [99/99])) [99/99]))
///                  Y))
///           (last (ivar_2 (subrange 0 99 nil nil) i))
///           (last (ivar_58 (subrange 1 100 nil nil) nil)) nil)))))
///  nil)

/// OUTPUT:
use std::rc::Rc;

#[allow(non_snake_case, dead_code)]
fn smalltranspose__transpose_step(
    mut ivar_1: Rc<[Rc<[i32; SIZE]>; SIZE]>,
    ivar_2: i32,
    ivar_3: i32
) -> Rc<[Rc<[i32; SIZE]>; SIZE]> {
    {
        let ivar_4: bool = { ivar_3 == SIZE as i32 };
        if ivar_4 {
            ivar_1
        } else {
            {
                let ivar_9: Rc<[Rc<[i32; SIZE]>; SIZE]> = {
                    {
                        let ivar_11: i32 = {
                            {
                                let ivar_16: Rc<[i32; SIZE]> = { ivar_1[ivar_3 as usize].clone() };
                                ivar_16[ivar_2 as usize].clone()
                            }
                        };
                        {
                            let ivar_12: i32 = {
                                {
                                    let ivar_27: Rc<[i32; SIZE]> = {
                                        ivar_1[ivar_2 as usize].clone()
                                    };
                                    ivar_27[ivar_3 as usize].clone()
                                }
                            };
                            {
                                let mut ivar_40: Rc<[Rc<[i32; SIZE]>; SIZE]> = {
                                    (*Rc::make_mut(
                                        &mut (*Rc::make_mut(&mut ivar_1))[ivar_2 as usize]
                                    ))[ivar_3 as usize] = ivar_11;
                                    ivar_1
                                };
                                (*Rc::make_mut(
                                    &mut (*Rc::make_mut(&mut ivar_40))[ivar_3 as usize]
                                ))[ivar_2 as usize] = ivar_12;
                                ivar_40
                            }
                        }
                    }
                };
                {
                    let ivar_58: i32 = { ivar_3 + 1 };
                    smalltranspose__transpose_step(ivar_9, ivar_2, ivar_58)
                }
            }
        }
    }
}