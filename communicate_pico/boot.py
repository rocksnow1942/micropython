# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
# import webrepl
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
gc.collect()
#start wift 
# webrepl.start()
machine.freq(160000000)
import network 
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)
def connect_wifi():
    wifipoints = {'Miaomiao': 'asdfghjkl', 'aptitude': 'aptitudewifi'}
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    stations = sta_if.scan()
    for station in stations:
        station_str = station[0].decode()
        if station_str in wifipoints:
            sta_if.connect(station_str, wifipoints[station_str])
            return True
    return False
connect_wifi()