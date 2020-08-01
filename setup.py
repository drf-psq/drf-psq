from setuptools import setup, find_packages


description = (
    "The simplest and most general way to manage method-based "
    "permissions, serializers, and querysets for the Django REST framework!"
)

setup(
    name='drf_psq',
    version='1.0.0',
    packages=find_packages(),

    description=description,
    license='MIT',
    author='AminHP',
    author_email='mdan.hagh@gmail.com',

    install_requires=[
        'django',
        'djangorestframework',
    ],
)
