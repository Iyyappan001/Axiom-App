[app]
title = LifeOS
version = 0.1.0
package.name = lifeos
package.domain = org.lifeos
source.dir = .
source.include_exts = py,kv,sql,md,png,jpg,ttf
# Keep the embedded Android interpreter aligned with the CI toolchain. An
# unpinned python3 lets p4a select newer CPython wheels independently.
requirements = python3==3.11.9,kivy,requests,charset-normalizer==3.4.3
orientation = portrait
android.permissions = INTERNET
android.api = 35
android.accept_sdk_license = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
