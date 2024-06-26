# -*- coding: utf-8 -*-
'''Everything returned by Veilchen()._cast() MUST be WSGI compatiple.'''

import unittest
import veilchen
from veilchen import tob, touni
from .tools import ServerTestBase, tobs, warn

USING_UJSON = True

try:
    import ujson
except ImportError:
    USING_UJSON = False

class TestOutputFilter(ServerTestBase):
    ''' Tests for WSGI functionality, routing and output casting (decorators) '''

    def test_bytes(self):
        self.app.route('/')(lambda: tob('test'))
        self.assertBody('test')

    def test_bytearray(self):
        self.app.route('/')(lambda: map(tob, ['t', 'e', 'st']))
        self.assertBody('test')

    def test_tuple(self):
        self.app.route('/')(lambda: ('t', 'e', 'st'))
        self.assertBody('test')

    def test_emptylist(self):
        self.app.route('/')(lambda: [])
        self.assertBody('')

    def test_none(self):
        self.app.route('/')(lambda: None)
        self.assertBody('')

    def test_illegal(self):
        self.app.route('/')(lambda: 1234)
        self.assertStatus(500)
        self.assertInBody('Unhandled exception')

    def test_error(self):
        veilchen.debug(True)
        self.app.route('/')(lambda: 1/0)
        self.assertStatus(500)
        self.assertInBody('ZeroDivisionError')

    def test_fatal_error(self):
        @self.app.route('/')
        def test(): raise KeyboardInterrupt()
        self.assertRaises(KeyboardInterrupt, self.assertStatus, 500)

    def test_file(self):
        self.app.route('/')(lambda: tobs('test'))
        self.assertBody('test')

    def test_unicode(self):
        self.app.route('/')(lambda: touni('äöüß'))
        self.assertBody(touni('äöüß').encode('utf8'))

        self.app.route('/')(lambda: [touni('äö'), touni('üß')])
        self.assertBody(touni('äöüß').encode('utf8'))

        @self.app.route('/')
        def test5():
            veilchen.response.content_type='text/html; charset=iso-8859-15'
            return touni('äöüß')
        self.assertBody(touni('äöüß').encode('iso-8859-15'))

        @self.app.route('/')
        def test5():
            veilchen.response.content_type='text/html'
            return touni('äöüß')
        self.assertBody(touni('äöüß').encode('utf8'))

    def test_json(self):
        self.app.route('/')(lambda: {'a': 1})

        self.assertBody(veilchen.json_dumps({'a': 1}))
        self.assertHeader('Content-Type','application/json')

    @unittest.skipIf(USING_UJSON, 'ujson do not throw exception in serialize')
    def test_json_serialization_error(self):
        """
        Verify that 500 errors serializing dictionaries don't return
        content-type application/json
        """
        self.app.route('/')(lambda: {'a': set()})

        self.assertStatus(500)
        self.assertHeader('Content-Type','text/html; charset=UTF-8')


    def test_json_HTTPResponse(self):
        self.app.route('/')(lambda: veilchen.HTTPResponse({'a': 1}, 500))

        self.assertBody(veilchen.json_dumps({'a': 1}))
        self.assertHeader('Content-Type','application/json')

    def test_json_HTTPError(self):
        self.app.error(400)(lambda e: e.body)
        self.app.route('/')(lambda: veilchen.HTTPError(400, {'a': 1}))

        self.assertBody(veilchen.json_dumps({'a': 1}))
        self.assertHeader('Content-Type','application/json')

    def test_generator_callback(self):
        @self.app.route('/')
        def test():
            veilchen.response.headers['Test-Header'] = 'test'
            yield 'foo'
        self.assertBody('foo')
        self.assertHeader('Test-Header', 'test')

    def test_empty_generator_callback(self):
        @self.app.route('/')
        def test():
            yield
            veilchen.response.headers['Test-Header'] = 'test'
        self.assertBody('')
        self.assertHeader('Test-Header', 'test')

    def test_error_in_generator_callback(self):
        @self.app.route('/')
        def test():
            yield 1/0
        self.assertStatus(500)
        self.assertInBody('ZeroDivisionError')

    def test_fatal_error_in_generator_callback(self):
        @self.app.route('/')
        def test():
            yield
            raise KeyboardInterrupt()
        self.assertRaises(KeyboardInterrupt, self.assertStatus, 500)

    def test_httperror_in_generator_callback(self):
        @self.app.route('/')
        def test():
            yield
            veilchen.abort(404, 'teststring')
        self.assertInBody('teststring')
        self.assertInBody('404 Not Found')
        self.assertStatus(404)

    def test_httpresponse_in_generator_callback(self):
        @self.app.route('/')
        def test():
            yield veilchen.HTTPResponse('test')
        self.assertBody('test')

    def test_unicode_generator_callback(self):
        @self.app.route('/')
        def test():
            yield touni('äöüß')
        self.assertBody(touni('äöüß').encode('utf8'))

    def test_invalid_generator_callback(self):
        @self.app.route('/')
        def test():
            yield 1234
        self.assertStatus(500)
        self.assertInBody('Unsupported response type')

    def test_iterator_with_close(self):
        class MyIter(object):
            def __init__(self, data):
                self.data = data
                self.closed = False
            def close(self):    self.closed = True
            def __iter__(self): return iter(self.data)

        byte_iter = MyIter([tob('abc'), tob('def')])
        unicode_iter = MyIter([touni('abc'), touni('def')])

        for test_iter in (byte_iter, unicode_iter):
            @self.app.route('/')
            def test(): return test_iter
            self.assertInBody('abcdef')
            self.assertTrue(byte_iter.closed)

    def test_cookie(self):
        """ WSGI: Cookies """
        @veilchen.route('/cookie')
        def test():
            veilchen.response.set_cookie('b', 'b')
            veilchen.response.set_cookie('c', 'c', path='/')
            return 'hello'
        try:
            c = self.urlopen('/cookie')['header'].get_all('Set-Cookie', '')
        except:
            c = self.urlopen('/cookie')['header'].get('Set-Cookie', '').split(',')
            c = [x.strip() for x in c]
        self.assertTrue('b=b' in c)
        self.assertTrue('c=c; Path=/' in c)
