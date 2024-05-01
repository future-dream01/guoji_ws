; Auto-generated. Do not edit!


(cl:in-package main-msg)


;//! \htmlinclude Yolox_data.msg.html

(cl:defclass <Yolox_data> (roslisp-msg-protocol:ros-message)
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

(cl:defclass Yolox_data (<Yolox_data>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Yolox_data>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Yolox_data)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name main-msg:<Yolox_data> is deprecated: use main-msg:Yolox_data instead.")))

(cl:ensure-generic-function 'target-val :lambda-list '(m))
(cl:defmethod target-val ((m <Yolox_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader main-msg:target-val is deprecated.  Use main-msg:target instead.")
  (target m))

(cl:ensure-generic-function 'x_p-val :lambda-list '(m))
(cl:defmethod x_p-val ((m <Yolox_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader main-msg:x_p-val is deprecated.  Use main-msg:x_p instead.")
  (x_p m))

(cl:ensure-generic-function 'y_p-val :lambda-list '(m))
(cl:defmethod y_p-val ((m <Yolox_data>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader main-msg:y_p-val is deprecated.  Use main-msg:y_p instead.")
  (y_p m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Yolox_data>) ostream)
  "Serializes a message object of type '<Yolox_data>"
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
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Yolox_data>) istream)
  "Deserializes a message object of type '<Yolox_data>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Yolox_data>)))
  "Returns string type for a message object of type '<Yolox_data>"
  "main/Yolox_data")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Yolox_data)))
  "Returns string type for a message object of type 'Yolox_data"
  "main/Yolox_data")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Yolox_data>)))
  "Returns md5sum for a message object of type '<Yolox_data>"
  "dd8ae1831add5d55430f288fc3367194")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Yolox_data)))
  "Returns md5sum for a message object of type 'Yolox_data"
  "dd8ae1831add5d55430f288fc3367194")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Yolox_data>)))
  "Returns full string definition for message of type '<Yolox_data>"
  (cl:format cl:nil "uint8 target~%float32 x_p~%float32 y_p~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Yolox_data)))
  "Returns full string definition for message of type 'Yolox_data"
  (cl:format cl:nil "uint8 target~%float32 x_p~%float32 y_p~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Yolox_data>))
  (cl:+ 0
     1
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Yolox_data>))
  "Converts a ROS message object to a list"
  (cl:list 'Yolox_data
    (cl:cons ':target (target msg))
    (cl:cons ':x_p (x_p msg))
    (cl:cons ':y_p (y_p msg))
))
