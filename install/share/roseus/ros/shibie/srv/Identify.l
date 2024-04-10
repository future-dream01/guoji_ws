;; Auto-generated. Do not edit!


(when (boundp 'shibie::Identify)
  (if (not (find-package "SHIBIE"))
    (make-package "SHIBIE"))
  (shadow 'Identify (find-package "SHIBIE")))
(unless (find-package "SHIBIE::IDENTIFY")
  (make-package "SHIBIE::IDENTIFY"))
(unless (find-package "SHIBIE::IDENTIFYREQUEST")
  (make-package "SHIBIE::IDENTIFYREQUEST"))
(unless (find-package "SHIBIE::IDENTIFYRESPONSE")
  (make-package "SHIBIE::IDENTIFYRESPONSE"))

(in-package "ROS")





(defclass shibie::IdentifyRequest
  :super ros::object
  :slots (_call ))

(defmethod shibie::IdentifyRequest
  (:init
   (&key
    ((:call __call) "")
    )
   (send-super :init)
   (setq _call (string __call))
   self)
  (:call
   (&optional __call)
   (if __call (setq _call __call)) _call)
  (:serialization-length
   ()
   (+
    ;; string _call
    4 (length _call)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _call
       (write-long (length _call) s) (princ _call s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _call
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _call (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass shibie::IdentifyResponse
  :super ros::object
  :slots (_target _x _y ))

(defmethod shibie::IdentifyResponse
  (:init
   (&key
    ((:target __target) 0)
    ((:x __x) 0)
    ((:y __y) 0)
    )
   (send-super :init)
   (setq _target (round __target))
   (setq _x (round __x))
   (setq _y (round __y))
   self)
  (:target
   (&optional __target)
   (if __target (setq _target __target)) _target)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:serialization-length
   ()
   (+
    ;; uint8 _target
    1
    ;; int64 _x
    8
    ;; int64 _y
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _target
       (write-byte _target s)
     ;; int64 _x
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _x (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _x) (= (length (_x . bv)) 2)) ;; bignum
              (write-long (ash (elt (_x . bv) 0) 0) s)
              (write-long (ash (elt (_x . bv) 1) -1) s))
             ((and (class _x) (= (length (_x . bv)) 1)) ;; big1
              (write-long (elt (_x . bv) 0) s)
              (write-long (if (>= _x 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _x s)(write-long (if (>= _x 0) 0 #xffffffff) s)))
     ;; int64 _y
#+(or :alpha :irix6 :x86_64)
       (progn (sys::poke _y (send s :buffer) (send s :count) :long) (incf (stream-count s) 8))
#-(or :alpha :irix6 :x86_64)
       (cond ((and (class _y) (= (length (_y . bv)) 2)) ;; bignum
              (write-long (ash (elt (_y . bv) 0) 0) s)
              (write-long (ash (elt (_y . bv) 1) -1) s))
             ((and (class _y) (= (length (_y . bv)) 1)) ;; big1
              (write-long (elt (_y . bv) 0) s)
              (write-long (if (>= _y 0) 0 #xffffffff) s))
             (t                                         ;; integer
              (write-long _y s)(write-long (if (>= _y 0) 0 #xffffffff) s)))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _target
     (setq _target (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; int64 _x
#+(or :alpha :irix6 :x86_64)
      (setf _x (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _x (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;; int64 _y
#+(or :alpha :irix6 :x86_64)
      (setf _y (prog1 (sys::peek buf ptr- :long) (incf ptr- 8)))
#-(or :alpha :irix6 :x86_64)
      (setf _y (let ((b0 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4)))
                  (b1 (prog1 (sys::peek buf ptr- :integer) (incf ptr- 4))))
              (cond ((= b1 -1) b0)
                     ((and (= b1  0)
                           (<= lisp::most-negative-fixnum b0 lisp::most-positive-fixnum))
                      b0)
                    ((= b1  0) (make-instance bignum :size 1 :bv (integer-vector b0)))
                    (t (make-instance bignum :size 2 :bv (integer-vector b0 (ash b1 1)))))))
   ;;
   self)
  )

(defclass shibie::Identify
  :super ros::object
  :slots ())

(setf (get shibie::Identify :md5sum-) "86f4e91a6ab25c36871755e93aece959")
(setf (get shibie::Identify :datatype-) "shibie/Identify")
(setf (get shibie::Identify :request) shibie::IdentifyRequest)
(setf (get shibie::Identify :response) shibie::IdentifyResponse)

(defmethod shibie::IdentifyRequest
  (:response () (instance shibie::IdentifyResponse :init)))

(setf (get shibie::IdentifyRequest :md5sum-) "86f4e91a6ab25c36871755e93aece959")
(setf (get shibie::IdentifyRequest :datatype-) "shibie/IdentifyRequest")
(setf (get shibie::IdentifyRequest :definition-)
      "string call
---
uint8 target
int64 x
int64 y
")

(setf (get shibie::IdentifyResponse :md5sum-) "86f4e91a6ab25c36871755e93aece959")
(setf (get shibie::IdentifyResponse :datatype-) "shibie/IdentifyResponse")
(setf (get shibie::IdentifyResponse :definition-)
      "string call
---
uint8 target
int64 x
int64 y
")



(provide :shibie/Identify "86f4e91a6ab25c36871755e93aece959")


