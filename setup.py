#!/usr/bin/env python

from setuptools import setup

import veilchen

setup(name='bottle',
      version=veilchen.__version__,
      description='Fast and simple WSGI-framework for small web-applications.',
      long_description=veilchen.__doc__,
      long_description_content_type="text/markdown",
      author="Oz Tiram",
      author_email='oz.tiram@gmail.com',
      url='http://bottlepy.org/',
      project_urls={
          'Source': 'https://github.com/bottlepy/bottle',
      },
      py_modules=['veilchen'],
      scripts=['veilechen.py'],
      license='MIT',
      platforms='any',
      classifiers=['Development Status :: 4 - Beta',
                   "Operating System :: OS Independent",
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
                   'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.9',
                   'Programming Language :: Python :: 3.10',
                   'Programming Language :: Python :: 3.11',
                   'Programming Language :: Python :: 3.12',
                   ],
      )
