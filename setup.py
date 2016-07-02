from setuptools import setup

setup(
    name='hail',
    version='0.3b1',
    py_modules=["hail"],


    author='Elisey Zanko',
    author_email='elisey.zanko@gmail.com',
    description='Pythonic bindings for the Apache Storm UI REST API',
    license='BSD-3-Clause',
    url='https://github.com/31z4/hail',

    test_suite='tests',
    tests_require='waiting'
)
