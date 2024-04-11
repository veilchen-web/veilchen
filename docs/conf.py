# -*- coding: utf-8 -*-
import sys
import os
import time

# Use the matching veilchen version, not a globally installed one.
veilchen_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.insert(0, veilchen_dir)
import veilchen

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.intersphinx',
              'sphinx.ext.viewcode',
              'sphinx_rtd_theme',]

html_theme = "sphinx_rtd_theme"

master_doc = 'index'
project = u'Veilchen'
copyright = u'2009-%s, %s' % (time.strftime('%Y'), veilchen.__author__)
version = ".".join(veilchen.__version__.split(".")[:2])
release = veilchen.__version__
add_function_parentheses = True
add_module_names = False
autodoc_member_order = 'bysource'
pygments_style = 'sphinx'
intersphinx_mapping = {'python': ('http://docs.python.org/', None),
                       'werkzeug': ('http://werkzeug.pocoo.org/docs/', None)}

locale_dirs = ['_locale/']
gettext_compact = False
