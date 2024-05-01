; Auto-generated. Do not edit!


(cl:in-package main-msg)


;//! \htmlinclude Result.msg.html

(cl:defclass <Result> (roslisp-msg-protocol:ros-message)
  ((target
    :reader target
    :initarg :target
    :type cl:fixnum
    :initform 0)
   (x_p
    :reader x_p
    :initarg :x_p
    :type cl:float
    :initform 0.0)
   (y_p
    :reader y_p
    :initarg :y_p
    :type cl:float
    :initform 0.0))
)

(cl:defclass Result (<Result>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Result>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Result)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name main-msg:<Result> is deprecated: use main-msg:Result instead.")))

(cl:ensure-generic-function 'target-val :lambda-list '(m))
(cl:defmethod target-val ((m <Result>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader main-msg:target-val is deprecated.  Use main-msg:target instead.")
  (target m))

(cl:ensure-generic-function 'x_p-val :lambda-list '(m))
(cl:defmethod x_p-val ((m <Result>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader main-msg:x_p-val is deprecated.  Use main-msg:x_p instead.")
  (x_p m))

(cl:ensure-generic-function 'y_p-val :lambda-list '(m))
(cl:defmethod y_p-val ((m <Result>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader main-msg:y_p-val is deprecated.  Use main-msg:y_p instead.")
  (y_p m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Result>) ostream)
  "Serializes a message object of type '<Result>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'target)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x_p))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'y_p))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Result>) istream)
  "Deserializes a message object of type '<Result>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'target)) (cl:read-byte istream))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x_p) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y_p) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Result>)))
  "Returns string type for a message object of type '<Result>"
  "main/Result")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Result)))
  "Returns string type for a message object of type 'Result"
  "main/Result")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Result>)))
  "Returns md5sum for a message object of type '<Result>"
  "dd8ae1831add5d55430f288fc3367194")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Result)))
  "Returns md5sum for a message object of type 'Result"
  "dd8ae1831add5d55430f288fc3367194")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Result>)))
  "Returns full string definition for message of type '<Result>"
  (cl:format cl:nil "uint8 target~%float32 x_p~%float32 y_p~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Result)))
  "Returns full string definition for message of type 'Result"
  (cl:format cl:nil "uint8 target~%float32 x_p~%float32 y_p~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Result>))
  (cl:+ 0
     1
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Result>))
  "Converts a ROS message object to a list"
  (cl:list 'Result
    (cl:cons ':target (target msg))
    (cl:cons ':x_p (x_p msg))
    (cl:cons ':y_p (y_p msg))
))
