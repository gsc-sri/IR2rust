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