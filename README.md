# WinRemote

This package is primarily a library which helps you remotely manage your
windows machine. Secondly it's command line tool to manage windows machine
remotely. The command line tool calls directly specific module. Modules are
very easily extensible. You can write your own and use it from command line
immediately, only specifying its name and module function.

For example this command:
```bash
$ winremote --username=X--password=Y--ip=IP services list
```

Equals to this python code:
```python
from winremote import winremote
import winrm
import pprint

session = winrm.Session(target=IP, auth=(X, Y))
win = winremote.Windows(session, winremote.WMI(session))
pprint.pprint(win.services.list())
```
