;; Auto-generated. Do not edit!


(when (boundp 'shibie::Yolox_action)
  (if (not (find-package "SHIBIE"))
    (make-package "SHIBIE"))
  (shadow 'Yolox_action (find-package "SHIBIE")))
(unless (find-package "SHIBIE::YOLOX_ACTION")
  (make-package "SHIBIE::YOLOX_ACTION"))

(in-package "ROS")
;;//! \htmlinclude Yolox_action.msg.html


(defclass shibie::Yolox_action
  :super ros::object
  :slots (_action ))

(defmethod shibie::Yolox_action
  (:init
   (&key
    ((:action __action) 0)
    )
   (send-super :init)
   (setq _action (round __action))
   self)
  (:action
   (&optional __action)
   (if __action (setq _action __action)) _action)
  (:serialization-length
   ()
   (+
    ;; uint8 _action
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _action
       (write-byte _action s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _action
     (setq _action (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get shibie::Yolox_action :md5sum-) "f1d6170759a11ac69d62121271b22bc9")
(setf (get shibie::Yolox_action :datatype-) "shibie/Yolox_action")
(setf (get shibie::Yolox_action :definition-)
      "uint8 action
")



(provide :shibie/Yolox_action "f1d6170759a11ac69d62121271b22bc9")


