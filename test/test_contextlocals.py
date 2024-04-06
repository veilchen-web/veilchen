# -*- coding: utf-8 -*-
'''
Some objects are context-local, meaning that they have different values depending on the context they are accessed from. A context is currently defined as a thread.
'''

import unittest
import veilchen
import threading


def run_thread(func):
    t = threading.Thread(target=func)
    t.start()
    t.join()

class TestThreadLocals(unittest.TestCase):
    def test_request(self):
        e1 = {'PATH_INFO': '/t1'}
        e2 = {'PATH_INFO': '/t2'}

        def run():
            veilchen.request.bind(e2)
            self.assertEqual(veilchen.request.path, '/t2')

        veilchen.request.bind(e1)
        self.assertEqual(veilchen.request.path, '/t1')
        run_thread(run)
        self.assertEqual(veilchen.request.path, '/t1')

    def test_response(self):

        def run():
            veilchen.response.bind()
            veilchen.response.content_type='test/thread'
            self.assertEqual(veilchen.response.headers['Content-Type'], 'test/thread')

        veilchen.response.bind()
        veilchen.response.content_type='test/main'
        self.assertEqual(veilchen.response.headers['Content-Type'], 'test/main')
        run_thread(run)
        self.assertEqual(veilchen.response.headers['Content-Type'], 'test/main')
