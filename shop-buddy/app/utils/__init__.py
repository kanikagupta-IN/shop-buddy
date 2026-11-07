# app/utils/__init__.py

"""
Utility modules for ShopBuddy AI, providing translation layers (i18n) 
and local file-based customer feedback storage.
"""

from .i18n import TRANSLATIONS
from .feedback_store import LocalFeedbackStore

# Explicitly define clean package exports for the application
__all__ = ["TRANSLATIONS", "LocalFeedbackStore"]
