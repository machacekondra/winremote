"""
This module implements work with system
"""


def get_process(session, name, attributes='Name,ProcessId'):
    """
    Description: return information about process

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param name: name of proccess
    :type name: str
    :param attributes: comma delimited name of attributes to be returned
    :type attributes: str
    :returns: info about process, None if process not found
    :rtype: dict
    """
    return session._wmi.query_first(
        "select %s from Win32_process where Name = '%s'" % (attributes, name)
    )


def list_processes(session, attributes='Name,ProcessId'):
    """
    Description: return list of all proccesses on windows machine

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param attributes: comma delimited name of attributes to be returned
    :type attributes: str
    :returns: list of processes info
    :rtype: list of dict
    """
    return session._wmi.query_first(
        "select %s from Win32_process" % attributes
    )


def arch(session):
    """
    Description: return windows architecture

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :returns: windows architecture (32-bit, 64-bit, ...)
    :rtype: str
    """
    return session._wmi.query_first(
        "select OSArchitecture from Win32_OperatingSystem"
    )['OSArchitecture']


def reboot(session):
    """
    Reboot windows machine

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :returns: True if cmd successfully ran, False otherwise
    :rtype: bool
    """
    return session.run_cmd('shutdown /r /t 1')[0]


def shutdown(session):
    """
    Shutdown windows machine

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :returns: True if cmd successfully ran, False otherwise
    :rtype: bool
    """
    return session.run_cmd('shutdown /s /t 1')[0]
