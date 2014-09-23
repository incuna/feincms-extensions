from setuptools import setup, find_packages


version = '0.3.0'


install_requires = (
    'FeinCMS>=1.9,<1.11',
)

setup(
    name='feincms-extensions',
    packages=find_packages(),
    package_data = {'feincms_extensions': ['templates/*']},
    version=version,
    description='',
    long_description='',
    author='Incuna',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/feincms-extensions/',
    install_requires=install_requires,
    zip_safe=False,
)
