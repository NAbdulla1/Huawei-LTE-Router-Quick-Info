from tkinter import Tk, W, E, Checkbutton, Frame, Label, Button, DISABLED, NORMAL
from threading import Thread
import time

from api_init import ApiInitializer
from window_mover import WindowMover
from minute_stat import LastKMinuteStat


class Application(Frame):
    def __init__(self, master):
        self.color1 = self._from_rgb(250, 250, 250)
        self.color2 = self._from_rgb(220, 220, 220)
        super().__init__(master, bg=self.color1)
        self.master = master
        self.pack()
        self.api = ApiInitializer('http://admin:qwerty5@192.168.8.1')
        self.last1MinuteStat = LastKMinuteStat(1)
        self._initUI()

    def _initUI(self):

        self.master.title("Quick Router Switch")

        self.cur_wifi_user_count = Label(self, bg=self.color1)
        self.cur_wifi_user_count.grid(row=0, column=0)

        self.signal_strength = Label(self, bg=self.color2)
        self.signal_strength.grid(row=0, column=1)

        self.last_1_minute_usage = Label(self, bg=self.color1)
        self.last_1_minute_usage.grid(row=0, column=2)

        self.data_conn_status = Checkbutton(
            self, text="Data\nConn", bg=self.color2)
        self.data_conn_status['command'] = self._toggle_data_connection_and_clear_stat
        self.data_conn_status.grid(row=0, column=3)

        self.battery_percentage = Label(self, bg=self.color1)
        self.battery_percentage.grid(row=0, column=4)

        self.gripBtn = Button(self, bitmap="gray25")
        self.gripBtn.grid(row=0, column=5)

        self.updateUI()
        self.pack()

    def updateUI(self):
        if self.isApiNone() or self.api.getClient().monitoring is None:
            self.last1MinuteStat.clear()
            self.cur_wifi_user_count['text'] = "No"
            self.signal_strength['text'] = "Wifi"
            self.data_conn_status.deselect()
            self.data_conn_status.config(state=DISABLED)
            self.battery_percentage['text'] = "Battery\nudf%"
            return

        status = self.api.getClient().monitoring.status()
        traffic_stat = self.api.getClient().monitoring.traffic_statistics()

        self.cur_wifi_user_count['text'] = "usr\n%2s" % status['CurrentWifiUser']
        self.signal_strength['text'] = self._get_network(
        ) + "\n" + self._get_signal_bars(status['SignalIcon'])
        self.last1MinuteStat.append(
            int(traffic_stat['CurrentUpload']), int(traffic_stat['CurrentDownload']))
        self.last_1_minute_usage['text'] = self.last1MinuteStat.getFormattedStat(
        )

        if self.data_conn_status['state'] == DISABLED:
            self.data_conn_status.config(state=NORMAL)
        if self._is_data_connected():
            self.data_conn_status.select()
        else:
            self.data_conn_status.deselect()

        self.battery_percentage['text'] = "Battery\n" + \
            status['BatteryPercent']+"%"

    def _is_data_connected(self):
        if self.isApiNone() or self.api.getClient().dial_up is None:
            return False
        return self.api.getClient().dial_up.mobile_dataswitch()["dataswitch"] == '1'

    def _toggle_data_connection_and_clear_stat(self):
        if self.isApiNone() or self.api.getClient().dial_up is None:
            self.data_conn_status.deselect()
            return
        if self._is_data_connected():
            self.api.getClient().dial_up.set_mobile_dataswitch('0')
            self.data_conn_status.deselect()
        else:
            self.api.getClient().dial_up.set_mobile_dataswitch('1')
            self.data_conn_status.select()
        self.last1MinuteStat.clear()

    def _get_signal_bars(self, num):
        bars = int(num)
        sig = ""
        for i in range(0, 5):
            if i < bars:
                sig += "|"
            else:
                sig += "."
        return sig

    def _get_network(self):
        if self.isApiNone() or self.api.getClient().device is None:
            return 'X'
        num = self.api.getClient().device.signal()['mode']
        if num is None:
            return 'X'
        elif num == '0':
            return "2G"
        elif num == '2':
            return "3G"
        else:
            return "4G"

    def _from_rgb(self, r, g, b):
        return "#%02x%02x%02x" % (r, g, b)

    def regularUIUpdater(self, sleepTime):
        while True:
            time.sleep(sleepTime)
            self.updateUI()

    def isApiNone(self):
        return self.api is None or self.api.getClient() is None


def main():
    root = Tk()
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.90)
    root.overrideredirect(True)
    app = Application(master=root)

    width = 235
    height = 40

    position = "%dx%d+%d+%d" % (width, height, root.winfo_screenwidth() -
                                width, root.winfo_screenheight()-height-30)
    root.geometry(position)

    updater = Thread(target=app.regularUIUpdater, args=(1,), daemon=True)
    updater.start()

    WindowMover(root, app.gripBtn)

    app.mainloop()


if __name__ == '__main__':
    main()
