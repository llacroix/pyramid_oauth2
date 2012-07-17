from setuptools import setup, find_packages

version = '0.12'

testing_extras = ['nose', 'coverage']
docs_extras = ['Sphinx']

setup(name='pyramid_oauth2',
      version=version,
      description="OAuth2 support for pyramid",
      long_description="""\
      """,
      classifiers=[],
      keywords='oauth2 pyramid',
      author='Lo\xc3\xafc Faure-Lacroix',
      author_email='lamerstar@gmail.com',
      url='delicieuxgateau.ca',
      license='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite="pyramid_oauth2",
      install_requires=[
          # -*- Extra requirements: -*-
          'pyramid',
      ],
      extras_require = {
          'dev':testing_extras,
          'docs':docs_extras,
          },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
