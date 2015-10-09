"""
This module implements work with products via WMI.
"""


def list(session, attributes='Name'):
    """
    Description: return list of all products installed on windows machine

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param attributes: comma delimited name of attributes to be returned
    :type attributes: str
    :returns: list of installed products
    :rtype: list of str
    """
    return session._wmi.query('select %s from win32_product' % attributes)


def get(session, name, attributes='Name'):
    """
    Description: return information about product @name

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param name: name of product to be searched
    :type name: str
    :param attributes: comma delimited name of attributes to be returned
    :type attributes: str
    :returns: info about product, None if product not found
    :rtype: dict
    """
    return session._wmi.query_first(
        "select %s from win32_product where Name = '%s'" % (attributes, name)
    )
