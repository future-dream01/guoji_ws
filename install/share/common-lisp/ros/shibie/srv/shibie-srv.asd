
(cl:in-package :asdf)

(defsystem "shibie-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Identify" :depends-on ("_package_Identify"))
    (:file "_package_Identify" :depends-on ("_package"))
  ))