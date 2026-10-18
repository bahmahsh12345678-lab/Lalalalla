[app]
title = WiFi Hacker
package.name = wifihacker
package.domain = com.lidraze
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 5.0
requirements = python3,kivy,pyjnius,android
orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_BACKGROUND_LOCATION,NEARBY_WIFI_DEVICES,CHANGE_NETWORK_STATE,WAKE_LOCK
android.api = 33
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
