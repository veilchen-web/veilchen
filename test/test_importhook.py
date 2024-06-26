# -*- coding: utf-8 -*-
import unittest
import sys, os
import veilchen

class TestImportHooks(unittest.TestCase):

    def make_module(self, name, **args):
        mod = sys.modules.setdefault(name, veilchen.new_module(name))
        mod.__file__ = '<virtual %s>' % name
        mod.__dict__.update(**args)
        return mod

    def test_direkt_import(self):
        mod = self.make_module('veilchen_test')
        import veilchen.ext.test
        self.assertEqual(veilchen.ext.test, mod)

    def test_from_import(self):
        mod = self.make_module('veilchen_test')
        from veilchen.ext import test
        self.assertEqual(test, mod)

    def test_data_import(self):
        mod = self.make_module('veilchen_test', item='value')
        from veilchen.ext.test import item
        self.assertEqual(item, 'value')

    def test_import_fail(self):
        ''' Test a simple static page with this server adapter. '''
        def test():
            import veilchen.ext.doesnotexist
        self.assertRaises(ImportError, test)

    def test_ext_isfile(self):
        ''' The virtual module needs a valid __file__ attribute.
            If not, the Google app engine development server crashes on windows.
        '''
        from veilchen import ext
        self.assertTrue(os.path.isfile(ext.__file__))
