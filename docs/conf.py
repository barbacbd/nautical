from nautical.release import __author__, __version__

project = "nautical"
author = __author__
version = __version__
release = __version__
copyright = f"2024, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx_mdinclude",
]

templates_path = ["_templates"]
exclude_patterns = ["build", "__pycache__"]

html_theme = "sphinx_rtd_theme"
html_static_path = []

autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__init__",
}

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
