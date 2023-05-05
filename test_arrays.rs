use std::rc::Rc;

const SIZE : usize = 1000;

#[allow(non_snake_case, dead_code)]
fn smalltranspose__transpose_step(
    ivar_1: Rc<[Rc<[i32; SIZE]>; SIZE]>,
    ivar_2: i32,
    ivar_3: i32
) -> Rc<[Rc<[i32; SIZE]>; SIZE]> {
    let ivar_4: bool = { ivar_3 == SIZE as i32 };
    if ivar_4 {
        ivar_1
    } else {
        let ivar_9: Rc<[Rc<[i32; SIZE]>; SIZE]> = {
            let ivar_11: i32 = {
                let ivar_16: Rc<[i32; SIZE]> = { ivar_1[ivar_3 as usize].clone() };
                ivar_16[ivar_2 as usize]
            };
            let ivar_12: i32 = {
                let ivar_27: Rc<[i32; SIZE]> = { ivar_1[ivar_2 as usize].clone() };
                ivar_27[ivar_3 as usize]
            };
            let ivar_47: Rc<[Rc<[i32; SIZE]>; SIZE]> = {
                let mut ivar_36: Rc<[i32; SIZE]> = { ivar_1[ivar_2 as usize].clone() };
                let mut ivar_44: Rc<[Rc<[i32; SIZE]>; SIZE]> = { ivar_1 };
                let ivar_45: Rc<[i32; SIZE]> = {
                    (*Rc::make_mut(&mut ivar_36))[ivar_3 as usize] = ivar_11;
                    ivar_36
                };
                (*Rc::make_mut(&mut ivar_44))[ivar_2 as usize] = ivar_45;
                ivar_44
            };
            let mut ivar_48: Rc<[i32; SIZE]> = { ivar_47[ivar_3 as usize].clone() };
            let mut ivar_56: Rc<[Rc<[i32; SIZE]>; SIZE]> = { ivar_47 };
            let ivar_57: Rc<[i32; SIZE]> = {
                (*Rc::make_mut(&mut ivar_48))[ivar_2 as usize] = ivar_12;
                ivar_48
            };
            (*Rc::make_mut(&mut ivar_56))[ivar_3 as usize] = ivar_57;
            ivar_56
        };
        let ivar_72: i32 = { ivar_3 + 1 };
        smalltranspose__transpose_step(ivar_9, ivar_2, ivar_72)
    }
}

#[allow(non_snake_case, dead_code)]
fn smalltranspose__transpose(
    ivar_1: Rc<[Rc<[i32; SIZE]>; SIZE]>,
    ivar_2: i32
) -> Rc<[Rc<[i32; SIZE]>; SIZE]> {
    let ivar_3: bool = { ivar_2 == SIZE as i32};
    if ivar_3 {
        ivar_1
    } else {
        let ivar_8: Rc<[Rc<[i32; SIZE]>; SIZE]> = {
            let ivar_21: i32 = { ivar_2 + 1 };
            smalltranspose__transpose_step(ivar_1, ivar_2, ivar_21)
        };
        let ivar_31: i32 = { ivar_2 + 1 };
        smalltranspose__transpose(ivar_8, ivar_31)
    }
}

#[allow(non_snake_case, dead_code)]
fn matrix_transpose(m: Vec<Vec<i32>>) -> Vec<Vec<i32>> {
    let mut t = vec![];
    let rows = m.len();
    let cols = m[0].len();
    for i in 0..cols {
        let mut row = vec![];
        for j in 0..rows {
            row.push(m[j][i]);
        }
        t.push(row);
    }
    t
}

fn main(){
    let array: [Rc<[i32; SIZE]>; SIZE] = core::array::from_fn(|i: usize| Rc::new(core::array::from_fn(|j: usize| (i as i32) + (j as i32))));
    let rc: Rc<[Rc<[i32; SIZE]>; SIZE]> = Rc::new(array);
    smalltranspose__transpose(rc, 0);

    //let t: Vec<Vec<i32>> = vec![vec![57; SIZE];SIZE];
    //matrix_transpose(t);
}