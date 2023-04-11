(lambda ((ivar_1 (subrange 0 * nil nil) n))
  '->
  (subrange 0 * nil nil)
  (let ivar_2
    boolean
    (let ivar_4
      (subrange 2 2 nil nil)
      2
      (< (ivar_1 (subrange 0 * nil nil) n)
         (last (ivar_4 (subrange 2 2 nil nil) nil)) nil))
    (if (ivar_2 boolean nil)
        (last (ivar_1 (subrange 0 * nil nil) n))
      (let ivar_7
        (subrange 0 * nil nil)
        (let ivar_15
          (subrange 0 * nil nil)
          (let ivar_11
            (subrange 1 1 nil nil)
            1
            (- (ivar_1 (subrange 0 * nil nil) n)
               (last (ivar_11 (subrange 1 1 nil nil) nil))
               (rename
                (((ivar_10 (subrange 0 * nil nil) nil) ivar_1
                  (subrange 0 * nil nil) n))
                in (subrange -1 * nil nil))))
          (is_prime__fibo (last (ivar_15 (subrange 0 * nil nil) nil))
           nil))
        (let ivar_8
          (subrange 0 * nil nil)
          (let ivar_22
            (subrange 0 * nil nil)
            (let ivar_18
              (subrange 2 2 nil nil)
              2
              (- (last (ivar_1 (subrange 0 * nil nil) n))
                 (last (ivar_18 (subrange 2 2 nil nil) nil))
                 (rename
                  (((ivar_17 (subrange 0 * nil nil) nil) ivar_1
                    (subrange 0 * nil nil) n))
                  in (subrange -2 * nil nil))))
            (is_prime__fibo (last (ivar_22 (subrange 0 * nil nil) nil))
             nil))
          (+ (last (ivar_7 (subrange 0 * nil nil) nil))
             (last (ivar_8 (subrange 0 * nil nil) nil))
             (subrange 0 * nil nil))))))
  nil)