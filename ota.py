import os
import time
import network
import machine
import uhashlib
import urequests


# # # # #  U S E R   V A R I A B L E   # # # # # #
#                                                #
#    ONLY UPDATE LINE NUMBER TWENTY TO ADAPT     #
#                                                #
# # # # #  U S E R   V A R I A B L E   # # # # # #


class ota:
    raw = "https://raw.githubusercontent.com"
    github = "https://github.com"

    def __init__(self, user="---", repo="---", url=None, branch="---", working_dir="---", files=["boot.py", "main.py"], headers={'User-Agent': '-----'}, ssid="---", password="---", timeout_sec=--):
        self.base_url = "{}/{}/{}".format(self.raw, user, repo) if user else url.replace(self.github, self.raw)
        self.url = url if url is not None else "{}/{}/{}".format(self.base_url, branch, working_dir)
        self.headers = headers
        self.files = files
        self.ssid = ssid
        self.password = password
        self.timeout_sec = timeout_sec

    def _check_hash(self, x, y):
        x_hash = uhashlib.sha1(x.encode())
        y_hash = uhashlib.sha1(y.encode())

        x = x_hash.digest()
        y = y_hash.digest()

        if str(x) == str(y):
            return True
        else:
            return False

    def _get_file(self, url):
        payload = urequests.get(url, headers=self.headers)
        code = payload.status_code

        if code == 200:
            return payload.text
        else:
            return None

    def _check_all(self):
        changes = []

        for file in self.files:
            latest_version = self._get_file(self.url + "/" + file)
            if latest_version is None:
                continue

            try:
                with open(file, "r") as local_file:
                    local_version = local_file.read()
            except:
                local_version = ""

            if not self._check_hash(latest_version, local_version):
                changes.append(file)

        return changes

    def state(self):
        # Returns true if at least one file update available
        if not self._check_all():
            print("no new update")
            return False
        else:
            print("update available")
            return True

    def update(self):
        # Updates and returns true if at least one file is updated
        changes = self._check_all()

        for file in changes:
            with open(file, "w") as local_file:
                local_file.write(self._get_file(self.url + "/" + file))

        if changes:
            print("files updated")
            return True
        else:
            print("no new update")
            return False

    def wificonnect(self):
        # Connects wifi and returns true if connected by timeout
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        if wlan.isconnected():
            pass
        else:
            print(f"connecting to network: {self.ssid}.")
            wlan.connect(self.ssid, self.password)
            start_time = time.time()
            while not wlan.isconnected() and (time.time() - start_time) < self.timeout_sec:
                print('.', end="")
                time.sleep(0.5)

        if wlan.isconnected():
            print("network connected")
            print("network config:", wlan.ifconfig())
            return True
        else:
            wlan.active(False)
            print("network unreachable")
            return False
