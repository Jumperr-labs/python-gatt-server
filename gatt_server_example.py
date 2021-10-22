from __future__ import print_function
import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

import array
try:
  from gi.repository import GObject
except ImportError:
  import gobject as GObject
import advertising
import gatt_server
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--adapter-name', type=str, help='Adapter name', default='')
    args = parser.parse_args()
    adapter_name = args.adapter_name

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    mainloop = GObject.MainLoop()

    advertising.advertising_main(mainloop, bus, adapter_name)
    gatt_server.gatt_server_main(mainloop, bus, adapter_name)
    mainloop.run()

if __name__ == '__main__':
    main()
