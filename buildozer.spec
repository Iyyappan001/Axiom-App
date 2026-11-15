[app]
title = LifeOS
version = 0.1.0
package.name = lifeos
package.domain = org.lifeos
source.dir = .
source.include_exts = py,kv,sql,md,png,jpg,ttf
# Match the hostpython3 recipe selected by the current p4a toolchain.
requirements = python3==3.14.2,kivy,requests,charset-normalizer==3.4.3
orientation = portrait
android.permissions = INTERNET
android.api = 35
android.accept_sdk_license = True
p4a.branch = develop

[buildozer]
log_level = 2
warn_on_root = 1
