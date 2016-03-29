import os
from os.path import join, dirname, abspath
from pip import req
from setuptools import setup, find_packages

import cli
from cli import main, conf

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = req.parse_requirements('requirements.txt', session=False)

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]


def generate_entry_scripts():
    """
    Generates the entry points for the ir-* scripts.
    """
    # 1 try to get spec names from the configuration
    # if cfg file is already provided
    specs = main.IRFactory.get_supported_specs(conf.config)
    if not specs:
        # 2 try to read from the file structure
        specs = next(os.walk(conf.config.get('defaults', 'settings')))[1]

    return ["ir-{0} = cli.main:entry_point".format(spec_name)
            for spec_name in
            specs]

prj_dir = dirname(abspath(__file__))
setup(
    name='infrared',
    version=cli.__VERSION__,
    packages=find_packages(),
    long_description=open(join(prj_dir, 'README.rst')).read(),
    entry_points={
        'console_scripts': generate_entry_scripts()
    },
    install_requires=reqs,
    author='Yair Fried',
    author_email='yfried@redhat.com'
)
