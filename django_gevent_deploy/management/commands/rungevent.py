from gevent import monkey; monkey.patch_all()
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.servers.basehttp import get_internal_wsgi_application
from gevent import wsgi
from gevent.pool import Pool


defaults = {
    'GEVENT_ADDR_PORT': '8000',
    'GEVENT_POOL_SIZE': None
}

class Command(BaseCommand):
    help = "Run gevent's WSGI serve Django project"
    args = '[port number or ipaddr:port] [pool size]'

    def handle(self, addr_port=None, pool_size=None, *args, **options):
        if args:
            raise CommandError('Usage: [ipaddr:]addr_port pool_size')

        addr_port = addr_port or getattr(settings, 'GEVENT_ADDR_PORT', defaults['GEVENT_ADDR_PORT'])
        pool_size = pool_size or getattr(settings, 'GEVENT_POOL_SIZE', defaults['GEVENT_POOL_SIZE'])

        try:
            addr, port = addr_port.split(':')
        except ValueError:
            addr, port = '', addr_port

        try:
            port = int(port)
        except ValueError:
            raise CommandError('Port must be an integer')

        if pool_size:
            try:
                pool_size = int(pool_size)
                pool = Pool(pool_size)
            except ValueError:
                raise CommandError('Spawn pool size must be an integer')
        else:
            pool = None

        wsgi_application = get_internal_wsgi_application()
        wsgi.WSGIServer((addr, port), wsgi_application, spawn=pool).serve_forever()

