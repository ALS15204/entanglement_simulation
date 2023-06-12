import setuptools
from pip._internal.req import parse_requirements

with open('README.md', 'r') as fh:
    long_description = fh.read()


def get_requirement(parsed_req):
    return parsed_req.requirement


requirements = [get_requirement(parsed_req) for parsed_req in parse_requirements('./requirements.txt', session='test')]

setuptools.setup(
    name='entanglement_simulation',
    version='1.0.0',
    author='Ronin Wu',
    author_email='roninwu@gmail.com',
    description='Simulate entanglement forging circuit for water molecule',
    long_description=long_description,
    url='https://github.com/ALS15204/entanglement_simulation',
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
    keywords='python quantum information entanglement forging',
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
