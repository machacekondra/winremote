"""
This module implements work with devices via WMI.
"""


def list(session, attributes='Name,ConfigManagerErrorCode'):
    """
    Description: return list of all devices on windows machine

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param attributes: comma delimited name of attributes to be returned
    :type attributes: str
    :returns: list of devices info
    :rtype: list of dict
    """
    return session._wmi.query('select %s from Win32_PnPEntity' % attributes)


def status(session, name):
    """
    Description: check status of device

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param name: name of the device to fetch info
    :type name: str
    :returns: True or False, True if device is OK, False otherwise
    :rtype: bool
    """
    dev = session._wmi.query_first(
        "select * from Win32_PnPEntity where Name = '%s'" % name
    )
    if dev and 'ConfigManagerErrorCode' in dev:
        return dev['ConfigManagerErrorCode'] == '0'

    return False


def get(session, name, attributes='Name'):
    """
    Description: get basic info about windows device @name

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param attributes: comma delimited name of attributes to be returned
    :type attributes: str
    :param name: name of the device to fetch info
    :type name: str
    :returns: dictionary with device driver information
    :returns: info about device, None if device not found
    :rtype: dict
    """
    return session._wmi.query_first(
        "select * from Win32_PnPEntity where Name = '%s'" % name
    )
