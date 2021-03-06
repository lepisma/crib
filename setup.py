from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = 'crib',
      version = '0.2.3',
      description = 'Minimal command line encryption for tiny notes',
      long_description = readme(),
      keywords = 'notes encryption minimal',
      url = 'http://github.com/lepisma/crib',
      author = 'lepisma',
      author_email = 'abhinav.tushar.vs@gmail.com',
      license = 'MIT',
      packages = ['crib'],
      install_requires = ['pycrypto'],
      entry_points={
          'console_scripts': ['crib = crib.command:main'],
      },
      include_package_data = True,
      zip_safe = False)
