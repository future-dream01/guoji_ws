;; Auto-generated. Do not edit!


(when (boundp 'shibie::Result)
  (if (not (find-package "SHIBIE"))
    (make-package "SHIBIE"))
  (shadow 'Result (find-package "SHIBIE")))
(unless (find-package "SHIBIE::RESULT")
  (make-package "SHIBIE::RESULT"))

(in-package "ROS")
;;//! \htmlinclude Result.msg.html


(defclass shibie::Result
  :super ros::object
  :slots (_target _x_p _y_p ))

(defmethod shibie::Result
  (:init
   (&key
    ((:target __target) 0)
    ((:x_p __x_p) 0.0)
    ((:y_p __y_p) 0.0)
    )
   (send-super :init)
   (setq _target (round __target))
   (setq _x_p (float __x_p))
   (setq _y_p (float __y_p))
   self)
  (:target
   (&optional __target)
   (if __target (setq _target __target)) _target)
  (:x_p
   (&optional __x_p)
   (if __x_p (setq _x_p __x_p)) _x_p)
  (:y_p
   (&optional __y_p)
   (if __y_p (setq _y_p __y_p)) _y_p)
  (:serialization-length
   ()
   (+
    ;; uint8 _target
    1
    ;; float32 _x_p
    4
    ;; float32 _y_p
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _target
       (write-byte _target s)
     ;; float32 _x_p
       (sys::poke _x_p (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _y_p
       (sys::poke _y_p (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _target
     (setq _target (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; float32 _x_p
     (setq _x_p (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _y_p
     (setq _y_p (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get shibie::Result :md5sum-) "dd8ae1831add5d55430f288fc3367194")
(setf (get shibie::Result :datatype-) "shibie/Result")
(setf (get shibie::Result :definition-)
      "uint8 target
float32 x_p
float32 y_p
")



(provide :shibie/Result "dd8ae1831add5d55430f288fc3367194")


