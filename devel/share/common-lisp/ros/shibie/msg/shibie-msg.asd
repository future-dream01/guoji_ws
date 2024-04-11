
(cl:in-package :asdf)

(defsystem "shibie-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Result" :depends-on ("_package_Result"))
    (:file "_package_Result" :depends-on ("_package"))
  ))