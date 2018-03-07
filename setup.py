from setuptools import setup

setup(name='complexity-estimator',
      version='0.1',
      description='Estimate function complexity',
      url='https://github.com/diwko/complexity-estimator',
      author='Dawid Siwko',
      author_email='dawidsiwko@gmail.com',
      license='MIT',
      packages=['complexityestimator'],
      entry_points={
          'console_scripts': [
              'complexity-estimator = complexityestimator.main:main'
          ]
      },
      zip_safe=False)
