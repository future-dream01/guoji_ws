; Auto-generated. Do not edit!


(cl:in-package shibie-srv)


;//! \htmlinclude Identify-request.msg.html

(cl:defclass <Identify-request> (roslisp-msg-protocol:ros-message)
  ((call
    :reader call
    :initarg :call
    :type cl:string
    :initform ""))
)

(cl:defclass Identify-request (<Identify-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Identify-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Identify-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name shibie-srv:<Identify-request> is deprecated: use shibie-srv:Identify-request instead.")))

(cl:ensure-generic-function 'call-val :lambda-list '(m))
(cl:defmethod call-val ((m <Identify-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader shibie-srv:call-val is deprecated.  Use shibie-srv:call instead.")
  (call m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Identify-request>) ostream)
  "Serializes a message object of type '<Identify-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'call))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'call))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Identify-request>) istream)
  "Deserializes a message object of type '<Identify-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'call) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'call) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Identify-request>)))
  "Returns string type for a service object of type '<Identify-request>"
  "shibie/IdentifyRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Identify-request)))
  "Returns string type for a service object of type 'Identify-request"
  "shibie/IdentifyRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Identify-request>)))
  "Returns md5sum for a message object of type '<Identify-request>"
  "86f4e91a6ab25c36871755e93aece959")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Identify-request)))
  "Returns md5sum for a message object of type 'Identify-request"
  "86f4e91a6ab25c36871755e93aece959")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Identify-request>)))
  "Returns full string definition for message of type '<Identify-request>"
  (cl:format cl:nil "string call~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Identify-request)))
  "Returns full string definition for message of type 'Identify-request"
  (cl:format cl:nil "string call~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Identify-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'call))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Identify-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Identify-request
    (cl:cons ':call (call msg))
))
;//! \htmlinclude Identify-response.msg.html

(cl:defclass <Identify-response> (roslisp-msg-protocol:ros-message)
  ((target
    :reader target
    :initarg :target
    :type cl:fixnum
    :initform 0)
   (x
    :reader x
    :initarg :x
    :type cl:integer
    :initform 0)
   (y
    :reader y
    :initarg :y
    :type cl:integer
    :initform 0))
)

(cl:defclass Identify-response (<Identify-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Identify-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Identify-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name shibie-srv:<Identify-response> is deprecated: use shibie-srv:Identify-response instead.")))

(cl:ensure-generic-function 'target-val :lambda-list '(m))
(cl:defmethod target-val ((m <Identify-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader shibie-srv:target-val is deprecated.  Use shibie-srv:target instead.")
  (target m))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <Identify-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader shibie-srv:x-val is deprecated.  Use shibie-srv:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <Identify-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader shibie-srv:y-val is deprecated.  Use shibie-srv:y instead.")
  (y m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Identify-response>) ostream)
  "Serializes a message object of type '<Identify-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'target)) ostream)
  (cl:let* ((signed (cl:slot-value msg 'x)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 18446744073709551616) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'y)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 18446744073709551616) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Identify-response>) istream)
  "Deserializes a message object of type '<Identify-response>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'target)) (cl:read-byte istream))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'x) (cl:if (cl:< unsigned 9223372036854775808) unsigned (cl:- unsigned 18446744073709551616))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'y) (cl:if (cl:< unsigned 9223372036854775808) unsigned (cl:- unsigned 18446744073709551616))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Identify-response>)))
  "Returns string type for a service object of type '<Identify-response>"
  "shibie/IdentifyResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Identify-response)))
  "Returns string type for a service object of type 'Identify-response"
  "shibie/IdentifyResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Identify-response>)))
  "Returns md5sum for a message object of type '<Identify-response>"
  "86f4e91a6ab25c36871755e93aece959")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Identify-response)))
  "Returns md5sum for a message object of type 'Identify-response"
  "86f4e91a6ab25c36871755e93aece959")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Identify-response>)))
  "Returns full string definition for message of type '<Identify-response>"
  (cl:format cl:nil "uint8 target~%int64 x~%int64 y~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Identify-response)))
  "Returns full string definition for message of type 'Identify-response"
  (cl:format cl:nil "uint8 target~%int64 x~%int64 y~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Identify-response>))
  (cl:+ 0
     1
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Identify-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Identify-response
    (cl:cons ':target (target msg))
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Identify)))
  'Identify-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Identify)))
  'Identify-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Identify)))
  "Returns string type for a service object of type '<Identify>"
  "shibie/Identify")