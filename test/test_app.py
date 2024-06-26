# -*- coding: utf-8 -*-
""" Tests for the functionality of the application object.

    TODO: Move other tests here.
""" 

import unittest
from veilchen import Veilchen

class TestApplicationObject(unittest.TestCase):
    
    def test_setattr(self):
        """ Attributed can be assigned, but only once. """
        app = Veilchen()
        app.test = 5
        self.assertEqual(5, app.test)
        self.assertRaises(AttributeError, setattr, app, 'test', 6) 
        del app.test
        app.test = 6
        self.assertEqual(6, app.test)
