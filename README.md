NGIMU-Python-Example
====================

This is an example Python script for sending and receiving OSC messages to and from an NGIMU over Wi-Fi.  The script will modify the device send IP address to send to that of the host machine and then display data from sensors, quaternion and battery messages.

![](https://github.com/xioTechnologies/NGIMU-Python-Example/blob/master/Screenshot.png)

### How to run

If you don't want to use a virtual environment
to keep your global package space clean, you
may skip the first and last steps. Otherwise:

```bash
python -m venv ENV
# For Windows:
source ENV/Scripts/activate
# For Linux
source ENV/bin/activate
pip install -r requirements.txt
# When done, deactivate
deactivate
```
