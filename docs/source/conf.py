# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import django

# -- Path setup --------------------------------------------------------------
# Localize a raiz do projeto a partir do arquivo atual `conf.py`.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

os.environ['DJANGO_SETTINGS_MODULE'] = 'siga.settings'
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SIGA'
copyright = '2024, SIGA - Sistema Integrado de Gestão Administrativa'
author = 'André Ventura'
release = '17/10/2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',    # Para documentar módulos automaticamente
    'sphinx.ext.viewcode',   # Para adicionar links para o código fonte
    'sphinx.ext.napoleon',   # Para suporte a Google style e NumPy style docstrings
]

templates_path = ['_templates']
exclude_patterns = []

language = 'pt_BR'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
