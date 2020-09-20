from setuptools import setup, find_packages

requires = [
    'flask',
    'requests',
    'python-dotenv',
    'numpy'
]

setup(
    name='auto-coins-reminder-bot',
    version='0.1',
    description='A tool to make trading easier',
    author='Candice Canoso',
    author_email='mail@cndce.me',
    keywords='flask binance crypto trading pse col coinsph',
    packages=find_packages(),
    include_package_data=True,
    install_requires=True
)