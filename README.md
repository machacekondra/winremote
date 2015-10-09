# WinRemote

This package is primarily a library which helps you remotely manage your
windows machine. Secondly it's command line tool to manage windows machine
remotely. The command line tool calls directly specific module. Modules are
very easily extensible. You can write your own and use it from command line
immediately, only specifying its name and module function.

For example this command:
```bash
$ winremote --username=Administrator --password=****** --ip=10.0.0.1 services get WinRM
{'Name': 'WinRM', 'StartMode': 'Auto', 'State': 'Running'}
```

Equals to this python code:
```python
import pprint
import winrm

from winremote import winremote
from winremote.modules import services

session = winrm.Session(target='10.0.0.1', auth=('Administrator', '******'))
pprint.pprint(
    services.get(
        winremote.Windows(session, winremote.WMI(session)),
        'WinRM'
    )
)
```

This package uses [pywinrm](https://pypi.python.org/pypi/pywinrm/),
so please follow its readme to setup your windows machine to work via WinRM.
