"""
This module implements work basic commands via WMI.
"""

# session is dynamically loaded
session = None


def __transfer_text(src_path, dest_path):
    content = ''
    with open(src_path) as f:
        content = f.read()
    content = content.replace('\n', '`r`n')

    r = session._session.run_ps(
        '$x = "%s" ; echo $x > %s' % (content, dest_path)
    )
    return not r.status_code, r.std_out, r.std_err


def copy_remote(src_path, dest_path):
    """
    Copy file from local machine to windows machine

    :param src_path: source path of file/directory on local machine
    :type src_path: str
    :param dest_path: destination path of file/directory on windows machine
    :type dest_path: str
    :returns: result of command, status_code, std_out, std_err
    :rtype: tuple
    """
    # TODO: Add support to transfer binary files
    return __transfer_text(src_path, dest_path)


def copy_local(src_path, dest_path):
    """
    Copy file/directory

    :param src_path: source path of file/directory
    :type src_path: str
    :param dest_path: destination path of file/directory
    :type dest_path: str
    :returns: result of command, status_code, std_out, std_err
    :rtype: tuple
    """
    return session.run_cmd('copy /Y "%s" "%s"' % (src_path, dest_path))


def make_dir(path):
    """
    Create directory

    :param path: path to directory
    :type path: str
    :returns: result of command, status_code, std_out, std_err
    :rtype: tuple
    """
    return session.run_cmd('mkdir "%s"' % path)


def remove_dir(path):
    """
    Remove directory

    :param path: path to directory
    :type path: str
    :returns: result of command, status_code, std_out, std_err
    :rtype: tuple
    """
    return session.run_cmd('rmdir "%s"' % path)


def cat_file(path):
    """
    Get file content

    :param path: path to file
    :type path: str
    :returns: content of file
    :rtype: str
    """
    return session.run_cmd('type "%s"' % path)[1]


def remove_file(path):
    """
    Remove file

    :param path: path to file
    :type path: str
    :returns: result of command, status_code, std_out, std_err
    :rtype: tuple
    """
    return session.run_cmd('del "%s"' % path)


def exists(path):
    """
    Check if file/directory exists

    :param path: path to file
    :type path: str
    :returns: True or False, True if file/dir exists False otherwise
    :rtype: bool
    """
    return session.run_cmd('dir /b "%s"' % path)[0]
