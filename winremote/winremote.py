import logging
import re
import winrm


class WMIError(Exception):
    """ Error occured while executing WMI command """


class WinRMException(Exception):
    """ Thrown when WinRMI don't work """


class Windows(object):

    def __init__(self, session, wmi):
        """
        Setup Windows object.

        :param session: session to winrm
        :type session: instance winrm.Session
        :param wmi: wmi instance to query windows via WMI
        :type wmi: instance WMI
        """
        self.logger = logging.getLogger('windows')
        self._session = session
        self._wmi = wmi

    def __getattr__(self, name):
        mod = getattr(
            __import__('modules', globals(), locals(), [name], -1),
            name,
        )
        setattr(mod, 'session', self)
        setattr(self, name, mod)
        return mod

    def run_cmd(self, cmd, params=[]):
        """
        Run command on windows.

        :param cmd: command to run
        :type cmd: str
        :param params: paramters of commands
        :type params: list
        :returns: result of command, status_code, std_out, std_err
        :rtype: tuple
        """
        r = self._session.run_cmd(cmd, params)
        self.logger.debug(
            'Running cmd: %s, Out: %s, Err: %s', cmd, r.std_out, r.std_err
        )
        if r.status_code:
            self.logger.error('Error running command %s: %s', cmd, r.std_err)

        return not r.status_code, r.std_out, r.std_err

    def is_connective(self):
        """
        Test if windows machine is accessible by running simple command.

        :return True if command was run successfully False if not
        :rtype: bool
        :raises WinRMException: if WinRM can't properly work
        """
        try:
            return not self._session.run_cmd('echo').status_code
        except (
            winrm.exceptions.WinRMTransportError,
            winrm.exceptions.TimeoutError
        ) as e:
            self.logger.warn("WinRM is not connective: %s", e)
            return False
        except (
            winrm.exceptions.WinRMWebServiceError,
            winrm.exceptions.WinRMAuthorizationError,
            winrm.exceptions.WinRMWSManFault,
            winrm.exceptions.UnauthorizedError
        ) as e:
            raise WinRMException(e)


class WMI(object):
    """
    Class provides access to windows machine via WMI.
    """
    re_arch = re.compile('^(?P<type>[0-9]+)-bit$', re.IGNORECASE)
    logger = logging.getLogger('wmi')

    def __init__(self, session):
        """
        Create a connection session to windows via winRM

        :param session: windows session
        """
        self._session = session

    def query_first(self, wql, timeout=120):
        """
        Function executes WQL query on remote machine.

        :param wql: wql query
        :type wql: str
        :param timeout: command timeout
        :type timeout: int
        :return: first item that matches query
        :rtype: dict
        """
        data = self.query(wql, timeout)
        return None if not data else data[0]

    def query(self, wql, timeout=120):
        """
        Function executes WQL query on remote machine.
        NOTE: This method does not support event queries.

        :param wql: wql query
        :type wql: str
        :param timeout: command timeout
        :type timeout: int
        :return: list of items
        :rtype: list
        """
        data = []
        r = self._session.run_ps('Get-WmiObject -Query "%s"' % wql)
        out, err = r.std_out.strip(), r.std_err
        self.logger.debug('Command: %s, Out: %s, Err: %s', wql, out, err)

        if r.status_code:
            raise WMIError(
                'Failed to execute wmi cmd "%s": res: %s, out: %s, err: %s' % (
                    wql, r.status_code, out, err
                )
            )
        if not out:
            return data

        for obj in out.split('\r\n\r\n'):
            dataObj = {}
            lastKey = None
            for line in obj.split('\r\n'):
                if line.startswith('__') or not line:
                    continue
                queryData = line.split(':')
                if len(queryData) > 1:
                    lastKey = queryData[0].strip()
                    dataObj[lastKey] = queryData[1].strip()
                else:
                    if lastKey:
                        dataObj[lastKey] += queryData[0].strip()
            data.append(dataObj)

        return data
