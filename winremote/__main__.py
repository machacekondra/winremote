import argparse
import logging
import pprint
import sys
import winrm
import winremote


def parse_args():
    parser = argparse.ArgumentParser(
        prog='windows',
        description='Tool to manage windows machine',
        epilog=(
            'Example: '
            'windows --username X --pasword Y --ip 10.0.0.2 services list'
        ),
    )
    parser.add_argument(
        '--username',
        required=True,
        help='username of user you want to connect with'
    )
    parser.add_argument(
        '--password',
        required=True,
        help="username's password",
    )
    parser.add_argument(
        '--ip',
        required=True,
        help='IP address of windows machine',
    )
    parser.add_argument(
        '--debug',
        default=False,
        action='store_true',
        help='enable debug log',
    )  # TODO
    parser.add_argument(
        'args',
        nargs='+',
        help=(
            'module & action & args to module, long options are used as kwargs'
        )
    )

    return parser.parse_known_args(sys.argv[1:])


def main():
    try:
        args, unknown = parse_args()
    except Exception as e:
        sys.stderr.write('Error: %s\n' % e)
        return 1

    ret = 1
    try:
        logging.basicConfig()
        logger = logging.getLogger('windows')

        session = winrm.Session(
            target=args.ip,
            auth=(args.username, args.password),
        )
        win = winremote.Windows(
            session,
            winremote.WMI(session),
        )

        kw = {}
        for i in unknown:
            if not i.startswith('--') or i.find('=') == -1:
                raise Exception(
                    "Invalid argument '%s'. Please check your command." % i
                )
            name, val = i.split('=')
            kw[name[2:]] = val

        pprint.pprint(
            getattr(
                getattr(win, args.args[0]),
                args.args[1],
            )(*args.args[2:], **kw)
        )
        ret = 0
    except Exception as e:
        logger.error(
            'Unexpected error while communicating with windows machine: %s', e
        )
        logger.debug('Exception', exc_info=True)
    return ret


if __name__ == "__main__":
    sys.exit(main())
