[app]

# (str) Title of your application
title = War

# (str) Package name, typically lowercase, no spaces or special chars
# >>> This is used internally on your device
package.name = war

# (str) Package domain (needed for android/ios packaging).
# >>> This should be a valid reverse-DNS domain, not an HTTPS link.
# >>> If you don’t own a domain, you can use something like "org.mywar" or "com.github.dollaralchemy.war"
package.domain = com.github.dollaralchemy.war

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (leave empty to include everything)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude
# source.exclude_exts = spec

# (list) Directories to exclude
# source.exclude_dirs = tests, bin, venv

# (list) Patterns to exclude
# source.exclude_patterns = *.exe, *.txt

# (str) Application version
version = 0.1

# (list) Application requirements
# >>> We only need the main libraries. Standard Python libs (os, datetime) don't need to be listed.
requirements = python3,kivy

# (str) Presplash or icon
# presplash.filename = %(source.dir)s/data/presplash.png
# icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations (landscape, portrait, etc.)
orientation = portrait

# (list) Services (like background services). Usually empty for a simple game
# services = NAME:ENTRYPOINT_TO_PY

#
# OSX Specific
#
osx.python_version = 3
osx.kivy_version = 1.9.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not (1 = yes, 0 = no)
# >>> For a mobile game, often you want fullscreen enabled.
fullscreen = 1

# (int) Target Android API (highest possible recommended, e.g. 31 or 33)
# >>> If you omit this, Buildozer picks a default. But specifying can help avoid warnings.
android.api = 33

# (int) Minimum API your APK will support
# >>> 21 = Android 5.0; you can raise if you only care about newer devices
android.minapi = 21

# (bool) AndroidX support (True if you have modern dependencies)
# android.enable_androidx = True

# (list) Permissions (INTERNET is typically needed if your app does any network calls)
# android.permissions = android.permission.INTERNET

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Indicate if the screen should stay on. If so, also add WAKE_LOCK permission
# android.wakelock = True

# (bool) Enable auto backup
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk).
android.release_artifact = aab

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

#
# Python-for-android (p4a) specific
#
# p4a.branch = master
# p4a.fork = kivy
# p4a.commit = HEAD

#
# iOS specific
#

# (bool) Whether or not to sign the code (set to True when you’re ready for App Store)
ios.codesign.allowed = false
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master


[buildozer]

# (int) Log level (0 = error, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1