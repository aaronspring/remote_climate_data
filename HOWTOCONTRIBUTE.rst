=====================
Contribution Guide
=====================

Contributions are highly welcomed and appreciated. Every little help counts,
so do not hesitate!

The following sections cover some general guidelines
regarding development in ``remote_climate_data`` for maintainers and contributors.
Nothing here is set in stone and can't be changed.
Feel free to suggest improvements or changes in the workflow.


How to contribute a new dataset
-------------------------------

- assign a new remote dataset to one of the catalogs: ``ocean``, ``land``, ``atmosphere`` or if nothing fits ``climate``
- assign a new remote shapefile to the ``shapefiles`` catalog
- try to add ``"simplecache::"`` to the ``urlpath`` to allow caching
- try to add documentation as URL and DOI in ``metadata``
- try to add informative quick plots to ``metadata.plot``
- try to account for many versions or variables with templating the ``urlpath`` with ``parameters``


Report bugs
-----------

Report bugs for ``remote_climate_data`` in the `issue tracker <https://github.com/aaronspring/remote_climate_data/issues>`_
with the label "bug".

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting,
  specifically the Python interpreter version and installed libraries.
* Detailed steps to reproduce the bug.


Fix bugs
--------

Look through the `GitHub issues for bugs <https://github.com/aaronspring/remote_climate_data/labels/bug>`_.

Talk to developers to find out how you can fix specific bugs.


Preparing Pull Requests
-----------------------


#. Fork the
   `remote_climate_data GitHub repository <https://github.com/aaronspring/remote_climate_data>`__.  It's
   fine to use ``remote_climate_data`` as your fork repository name because it will live
   under your user.

#. Clone your fork locally using `git <https://git-scm.com/>`_, connect your repository
   to the upstream (main project), and create a branch::

    $ git clone git@github.com:YOUR_GITHUB_USERNAME/remote_climate_data.git
    $ cd remote_climate_data
    $ git remote add upstream git@github.com:aaronspring/remote_climate_data.git

    # now, to fix a bug or add feature create your own branch off "master":

    $ git checkout -b your-bugfix-feature-branch-name master

   If you need some help with Git, follow this quick start
   guide: https://git.wiki.kernel.org/index.php/QuickStart

#. Install dependencies into a new conda environment::

    $ conda env update -f ci/environment-dev-3.7.yml
    $ conda activate remote_climate_data-dev

#. Make an editable install of remote_climate_data by running::

    $ pip install -e .


#. Break your edits up into reasonably sized commits::

    $ git commit -a -m "<commit message>"
    $ git push -u


#. Create a new changelog entry in ``CHANGELOG.rst``:

   - The entry should be entered as:

    <description> (``:pr:`#<pull request number>```) ```<author's names>`_``

    where ``<description>`` is the description of the PR related to the change and
    ``<pull request number>`` is the pull request number and ``<author's names>`` are your first
    and last names.


#. Finally, submit a pull request through the GitHub website using this data::

    head-fork: YOUR_GITHUB_USERNAME/remote_climate_data
    compare: your-branch-name

    base-fork: aaronspring/remote_climate_data
    base: master

Note that you can create the Pull Request while you're working on this. The PR will update
as you add more commits. ``remote_climate_data`` developers and contributors can then review your code
and offer suggestions.
