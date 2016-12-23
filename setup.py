from setuptools import setup

install_requires = ['Flask>=0.12', 'ZODB>=5.1.1']

setup(
    name="flask-zodb2", version="0.0.1", packages=['flask_zodb2'], include_package_data=True, zip_safe=False,
    install_requires=install_requires
)
