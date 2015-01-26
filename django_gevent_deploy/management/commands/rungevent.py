from gevent import monkey

monkey.patch_all()

# all imports after here

from gevent import wait

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.servers.basehttp import get_internal_wsgi_application
from gevent import wsgi, pywsgi
from gevent.pool import Pool


defaults = {
    'GEVENT_ADDR_PORT': '8000',
    'GEVENT_SECURE_ADDR_PORT': None,
    'GEVENT_SECURE_CERTIFICATE': None,
    'GEVENT_SECURE_PRIVATE_KEY': None,
    'GEVENT_POOL_SIZE': None,
}


class Command(BaseCommand):
    help = "Run gevent's WSGI serve Django project"
    args = '[port number or ipaddr:port] [pool size]'
    option_list = BaseCommand.option_list + (
        make_option(
            '--pool-size',
            default=None,
            help='Pool size to use for django-gevent-deploy.'
        ),
        make_option(
            '--certificate',
            default=None,
            help='SSL/TLS certificate to use for HTTPS server in django-gevent-deploy.'
        ),
        make_option(
            '--private-key',
            default=None,
            help='SSL/TLS private key to use for HTTPS server in django-gevent-deploy.'
        ),
        make_option(
            '--insecure',
            action='store_true',
            default=False,
            help='Allow to run HTTPS server by explicitly acknowledging '
                 'that doing so is insecure in django-gevent-deploy.'
        ),
    )

    def handle(self, addr_port=None, secure_addr_port=None, *args, **options):
        if args:
            raise CommandError('Usage: [ipaddr:]addr_port pool_size')

        addr_port = addr_port or getattr(
            settings, 'GEVENT_ADDR_PORT', defaults['GEVENT_ADDR_PORT']
        )
        secure_addr_port = secure_addr_port or getattr(
            settings, 'GEVENT_SECURE_ADDR_PORT', defaults['GEVENT_SECURE_ADDR_PORT']
        )
        certificate = options.get('certificate') or getattr(
            settings, 'GEVENT_SECURE_CERTIFICATE', defaults['GEVENT_SECURE_CERTIFICATE']
        )
        private_key = options.get('private_key') or getattr(
            settings, 'GEVENT_SECURE_PRIVATE_KEY', defaults['GEVENT_SECURE_PRIVATE_KEY']
        )
        pool_size = options.get('pool_size') or getattr(
            settings, 'GEVENT_POOL_SIZE', defaults['GEVENT_POOL_SIZE']
        )

        # HTTP configuration
        try:
            addr, port = addr_port.split(':')
        except ValueError:
            addr, port = '', addr_port

        try:
            port = int(port)
        except ValueError:
            raise CommandError('Port must be an integer')

        # HTTPS configuration
        secure_addr, secure_port = None, None
        if secure_addr_port:
            if not certificate:
                raise CommandError(
                    'You must specify certificate in order to use HTTPS server.'
                )

            if not private_key:
                raise CommandError(
                    'You must specify private key in order to use HTTPS server.'
                )

            if not options.get('insecure'):
                msg = (
                    'Are you absolutely sure you want to start HTTPS server '
                    'using django-gevent-deploy even though it is probably insecure? '
                    '[NO/yes]: '
                )
                if raw_input(msg).lower() not in ('y', 'yes'):
                    raise CommandError(
                        'You cannot run HTTPS server without explicitly acknowledging '
                        'that doing so is probably insecure!'
                    )

            try:
                secure_addr, secure_port = secure_addr_port.split(':')
            except ValueError:
                secure_addr, secure_port = '', secure_addr_port

            try:
                secure_port = int(secure_port)
            except ValueError:
                raise CommandError('HTTPS port must be an integer')

        # server configuration
        if pool_size:
            try:
                pool_size = int(pool_size)
                pool = Pool(pool_size)
            except ValueError:
                raise CommandError('Spawn pool size must be an integer')
        else:
            pool = 'default'

        wsgi_application = get_internal_wsgi_application()
        http = wsgi.WSGIServer((addr, port), wsgi_application, spawn=pool)

        if not secure_addr_port:
            pass
            http.serve_forever()

        else:
            http.start()

            # cant use wsgi here since it does not support SSL
            # in latest gevent version it does not matter but still...
            https = pywsgi.WSGIServer(
                (secure_addr, secure_port), wsgi_application, spawn=pool,
                keyfile=private_key, certfile=certificate,
            )
            https.start()

            wait()
