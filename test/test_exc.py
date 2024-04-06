import veilchen
from .tools import ServerTestBase

class TestError(Exception):
    pass

class TestAppException(ServerTestBase):

    def test_no_exc(self):
        @veilchen.route('/')
        def test(): return 'test'
        self.assertBody('test', '/')

    def test_memory_error(self):
        @veilchen.route('/')
        def test(): raise MemoryError
        self.assertRaises(MemoryError)

    def test_other_error(self):
        @veilchen.route('/')
        def test(): raise TestError
        self.assertRaises(TestError)

    def test_noncatched_error(self):
        @veilchen.route('/')
        def test(): raise TestError
        veilchen.request.environ['exc_info'] = None
        veilchen.catchall = False
        self.assertStatus(500, '/')
        self.assertInBody('TestError')
