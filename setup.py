# to install as module run 'pip3 install -e <path_to_project_root>'

from setuptools import setup, find_packages

setup(name='geodjango_news_map',
      version='1.0',
      packages=find_packages(),
      scripts=['manage.py']) # optional, places manage.py on $PATH
