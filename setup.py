from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install import INSTALL_SCHEMES
import os
import sys

python_exe = os.path.join(sys.prefix, "python.exe")
vuuvv_bat = '"%s" "%s"' % (python_exe, os.path.join(sys.prefix, "Scripts", "vuuvv"))
vuuvv = """#!%s
%s
"""

with open("vuuvv.py", "r") as f:
	vuuvv = vuuvv % (python_exe, f.read())

def create_vuuvv_bat():
	filename = os.path.join("bin", "vuuvv.bat")
	f = open(filename, "w")
	f.write(vuuvv_bat)
	f.close()

def create_vuuvv():
	filename = os.path.join("bin", "vuuvv")
	f = open(filename, "w")
	f.write(vuuvv)
	f.close()

if not os.path.isdir('bin'):
	os.mkdir('bin')
create_vuuvv_bat()
create_vuuvv()

setup(
	name = "vuuvv",
	version = "0.0.1",
	url = 'https://github.com/vuuvv/vuuvv',
	author = 'Vuuvv Software Foundation',
	author_email = 'vuuvv@qq.com',
	description = 'A web framework using flask, like ror.',
	#download_url = 'http://media.djangoproject.com/releases/1.3/Django-1.3.1.tar.gz',
	packages = ["vuuvv", "vuuvv.db", "vuuvv.tasks"],
	scripts = ['bin/vuuvv', 'bin/vuuvv.bat'],
	classifiers = ['Development Status :: 2 - Pre-Alpha',
				'Environment :: Web Environment',
				'Intended Audience :: Developers',
				'License :: OSI Approved :: BSD License',
				'Operating System :: OS Independent',
				'Programming Language :: Python',
				'Programming Language :: Python :: 2.6',
				'Programming Language :: Python :: 2.7',
				'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
				'Topic :: Software Development :: Libraries :: Python Modules'
 				],
)
