"""
This module implements work with files and basic cli commands.
"""


def __transfer_text(session, src_path, dest_path):
    content = ''
    with open(src_path) as f:
        content = f.read()
    content = content.replace('\n', '`r`n')

    r = session._session.run_ps(
        '$x = "%s" ; echo $x > %s' % (content, dest_path)
    )
    return not r.status_code, r.std_out, r.std_err


def copy_remote(session, src_path, dest_path):
    """
    Copy file from local machine to windows machine

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param src_path: source path of file/directory on local machine
    :type src_path: str
    :param dest_path: destination path of file/directory on windows machine
    :type dest_path: str
    :returns: result of command, status_code, std_out, std_err
    :rtype: tuple
    """
    # TODO: Add support to transfer binary files
    return __transfer_text(src_path, dest_path)


def copy_local(session, src_path, dest_path):
    """
    Copy file/directory

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param src_path: source path of file/directory
    :type src_path: str
    :param dest_path: destination path of file/directory
    :type dest_path: str
    :returns: result of command, status_code, std_out, std_err
    :rtype: tuple
    """
    return session.run_cmd('copy /Y "%s" "%s"' % (src_path, dest_path))


def make_dir(session, path):
    """
    Create directory

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param path: path to directory
    :type path: str
    :returns: result of command, status_code, std_out, std_err
    :rtype: tuple
    """
    return session.run_cmd('mkdir "%s"' % path)


def remove_dir(session, path):
    """
    Remove directory

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param path: path to directory
    :type path: str
    :returns: result of command, status_code, std_out, std_err
    :rtype: tuple
    """
    return session.run_cmd('rmdir "%s"' % path)


def cat_file(session, path):
    """
    Get file content

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param path: path to file
    :type path: str
    :returns: content of file
    :rtype: str
    """
    return session.run_cmd('type "%s"' % path)[1]


def remove_file(session, path):
    """
    Remove file

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param path: path to file
    :type path: str
    :returns: result of command, status_code, std_out, std_err
    :rtype: tuple
    """
    return session.run_cmd('del "%s"' % path)


def exists(session, path):
    """
    Check if file/directory exists

    :param session: instance of Windows, which hold session to win machine
    :type session: winremote.Windows
    :param path: path to file
    :type path: str
    :returns: True or False, True if file/dir exists False otherwise
    :rtype: bool
    """
    return session.run_cmd('dir /b "%s"' % path)[0]
