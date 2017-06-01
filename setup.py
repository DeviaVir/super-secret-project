from setuptools import setup, find_packages

requires = [req for req in open('requirements.txt').read().splitlines()
            if not req.startswith('git')]

setup(name='project',
      version='0.0.1',
      description='Super Duper Secret Project',
      long_description=open('README.md').read(),
      entry_points={
          'console_scripts': ['project=project.main:run'],
      },
      url='https://github.com/deviavir/project',
      author='Chase Sillevis',
      author_email='chase@sillevis.net',
      license='MIT',
      package_dir={'': 'src'},
      packages=find_packages('src', exclude=['test']),
      install_requires=requires,
      zip_safe=True)
