# Sphinx Setup

1. Download sphinx and the rinohtype extension

    `pip install Sphinx rinohtype sphinx-rtd-theme`

2. Make a directory for the documentation. You can use docs here, but you may wish to create a new folder.

    `mkdir example-docs`

3. Move to that directory

    `cd example-docs`

4. Generate the sphinx startup documentation:

    `sphinx-quickstart`

5. You may wish to use the configuration file provided or you may write your own. If you are writing you own add 
the following line to the configuration.py

    `extensions = ['sphinx.ext.autodoc', 'rinoh.frontend.sphinx', 'sphinx_rtd_theme']`

6. Uncomment the following lines 

    ```python
    import os
    import sys
    sys.path.insert(0, os.path.abspath('../..'))
    ```

7. In the block above, please set the absolute path to the base directory of the nautical project.

8. Add the following line after the block above:

    `sys.setrecursionlimit(1500)`

9. Add the html_theme by replacing/adding the line below to the configuration file:

    `html_theme = "sphinx_rtd_theme"`

10. You may also wish to change the documentation style. The `index.rst` file provides a basic documentation setup. 
You may use the file or generate your own.

11. Make the html page.

    `make html`

12. Run the build with rinohtype

    `sphinx-build -b rinoh source _build/rinoh`

13. You can find the html page inside of `example-docs/build/html/index.html`

14. You can find a pdf inside of `example-docs/_build/rinoh/{project}.pdf`

*If your python > 3.7 the latex generator for rinoh will fail*
