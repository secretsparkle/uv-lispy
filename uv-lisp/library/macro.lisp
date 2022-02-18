
(defmacro my-if (condition tr fa)
  `(cond (,condition ,tr)
         (t ,fa)))

(if (> 10 2)
    t
    nil)


(my-if (> 10 2)
       t
       nil)
