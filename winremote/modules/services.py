"""
This module implements work with services via WMI.
"""


def list(session, attributes='Name,State,StartMode'):
    """
    Description: return list of all services on windows machine

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param attributes: comma delimited name of attributes to be returned
    :type attributes: str
    :returns: list of services info
    :rtype: list of dict
    """
    return session._wmi.query('select %s from Win32_service' % attributes)


def get(session, name, attributes='Name,State,StartMode'):
    """
    Description: return information about service @name

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param name: name of service to be searched
    :type name: str
    :param attributes: comma delimited name of attributes to be returned
    :type attributes: str
    :returns: info about service, None if service not found
    :rtype: dict
    """
    return session._wmi.query_first(
        "select %s from Win32_service where Name = '%s'" % (attributes, name)
    )
