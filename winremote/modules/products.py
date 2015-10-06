"""
This module implements work with products via WMI.
"""

# session is dynamically loaded
session = None


def list(attributes='Name'):
    """
    Description: return list of all products installed on windows machine

    :param attributes: comma delimited name of attributes to be returned
    :type attributes: str
    :returns: list of installed products
    :rtype: list of str
    """
    return session._wmi.query('select %s from win32_product' % attributes)


def get(name, attributes='Name'):
    """
    Description: return information about product @name

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
