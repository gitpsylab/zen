import ota
import machine


ota = ota.ota(
  user="gitpsylab",
  repo="zen",
  branch="main",
  working_dir="zen",
  files = ["boot.py", "main.py"]
)

ota.wificonnect()

if ota.update():
    print("update complete.. rebooting...")
    machine.reset()
