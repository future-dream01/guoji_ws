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
  :slots (_back ))

(defmethod shibie::IdentifyResponse
  (:init
   (&key
    ((:back __back) "")
    )
   (send-super :init)
   (setq _back (string __back))
   self)
  (:back
   (&optional __back)
   (if __back (setq _back __back)) _back)
  (:serialization-length
   ()
   (+
    ;; string _back
    4 (length _back)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _back
       (write-long (length _back) s) (princ _back s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _back
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _back (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass shibie::Identify
  :super ros::object
  :slots ())

(setf (get shibie::Identify :md5sum-) "7debc7ecb9cc5cb9fe2af4ff555737b7")
(setf (get shibie::Identify :datatype-) "shibie/Identify")
(setf (get shibie::Identify :request) shibie::IdentifyRequest)
(setf (get shibie::Identify :response) shibie::IdentifyResponse)

(defmethod shibie::IdentifyRequest
  (:response () (instance shibie::IdentifyResponse :init)))

(setf (get shibie::IdentifyRequest :md5sum-) "7debc7ecb9cc5cb9fe2af4ff555737b7")
(setf (get shibie::IdentifyRequest :datatype-) "shibie/IdentifyRequest")
(setf (get shibie::IdentifyRequest :definition-)
      "string call
---
string back
")

(setf (get shibie::IdentifyResponse :md5sum-) "7debc7ecb9cc5cb9fe2af4ff555737b7")
(setf (get shibie::IdentifyResponse :datatype-) "shibie/IdentifyResponse")
(setf (get shibie::IdentifyResponse :definition-)
      "string call
---
string back
")



(provide :shibie/Identify "7debc7ecb9cc5cb9fe2af4ff555737b7")


