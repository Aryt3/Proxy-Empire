# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Proxy-Empire"
copyright = "2025, Aryt3 and 54toshi"
author = "Aryt3 and 54toshi"
release = "0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinxext.opengraph",
    "sphinx_sitemap",
    "sphinx_copybutton",
]

language = "en"
master_doc = "index"
pygments_style = "sphinx"
source_suffix = ".md"
templates_path = ["_templates"]

templates_path = ["_templates"]
exclude_patterns = []


# -- SEO ---------------------------------------------------------------------
# Open Graph: https://sphinxext-opengraph.readthedocs.io/
# ogp_site_url = "http://example.org/"
# ogp_image = "http://example.org/image.png"
ogp_description_length = 300
# ogp_type = "article"  # default: website

ogp_custom_meta_tags = [
    '<meta property="og:ignore_canonical" content="true" />',
]

ogp_enable_meta_description = True

myst_html_meta = {
    "description lang=en": "A tool to periodically fetch new proxies from various sources, validate and filter them and provide them for further usage",
    "keywords": "Proxy-Empire, Proxy, ProxyBroker, proxyscraper",
    "property=og:locale":  "en_US",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_title = "Proxy-Empire"
# html_favicon = "static/favicon.png"
html_baseurl = "https://proxy-empire.readthedocs.io/"
html_theme_options = {
#    "light_css_variables": {
#        "color-brand-primary": "red",
#        "color-brand-content": "#CC3333",
#        "color-admonition-background": "orange",
#    },
#    "announcement": "<em>Important</em> announcement!",
}
# html_logo = "logo.png"
html_static_path = ["_static"]
