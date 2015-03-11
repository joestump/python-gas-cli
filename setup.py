from setuptools import setup, find_packages


setup(
    name='gas',
    version='0.0.1',
    description='A Google Apps Add-on for Google Docs Spreadsheets that loads items from the API into a sheet.',
    long_description='',
    keywords='google',
    author='Joseph C. Stump',
    author_email='joe@stu.mp',
    url='https://github.com/joestump/python-gas-cli',
    license='BSD',
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'gas = gas.__main__:main',
        ],
    },
    install_requires=[
        'google-api-python-client'
    ],
    include_package_data=True
)
