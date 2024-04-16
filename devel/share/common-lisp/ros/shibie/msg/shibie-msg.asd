
(cl:in-package :asdf)

(defsystem "shibie-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Yolox_action" :depends-on ("_package_Yolox_action"))
    (:file "_package_Yolox_action" :depends-on ("_package"))
    (:file "Yolox_data" :depends-on ("_package_Yolox_data"))
    (:file "_package_Yolox_data" :depends-on ("_package"))
  ))