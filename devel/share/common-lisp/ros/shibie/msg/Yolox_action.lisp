; Auto-generated. Do not edit!


(cl:in-package shibie-msg)


;//! \htmlinclude Yolox_action.msg.html

(cl:defclass <Yolox_action> (roslisp-msg-protocol:ros-message)
  ((action
    :reader action
    :initarg :action
    :type cl:fixnum
    :initform 0))
)

(cl:defclass Yolox_action (<Yolox_action>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Yolox_action>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Yolox_action)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name shibie-msg:<Yolox_action> is deprecated: use shibie-msg:Yolox_action instead.")))

(cl:ensure-generic-function 'action-val :lambda-list '(m))
(cl:defmethod action-val ((m <Yolox_action>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader shibie-msg:action-val is deprecated.  Use shibie-msg:action instead.")
  (action m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Yolox_action>) ostream)
  "Serializes a message object of type '<Yolox_action>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'action)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Yolox_action>) istream)
  "Deserializes a message object of type '<Yolox_action>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'action)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Yolox_action>)))
  "Returns string type for a message object of type '<Yolox_action>"
  "shibie/Yolox_action")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Yolox_action)))
  "Returns string type for a message object of type 'Yolox_action"
  "shibie/Yolox_action")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Yolox_action>)))
  "Returns md5sum for a message object of type '<Yolox_action>"
  "f1d6170759a11ac69d62121271b22bc9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Yolox_action)))
  "Returns md5sum for a message object of type 'Yolox_action"
  "f1d6170759a11ac69d62121271b22bc9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Yolox_action>)))
  "Returns full string definition for message of type '<Yolox_action>"
  (cl:format cl:nil "uint8 action~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Yolox_action)))
  "Returns full string definition for message of type 'Yolox_action"
  (cl:format cl:nil "uint8 action~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Yolox_action>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Yolox_action>))
  "Converts a ROS message object to a list"
  (cl:list 'Yolox_action
    (cl:cons ':action (action msg))
))
