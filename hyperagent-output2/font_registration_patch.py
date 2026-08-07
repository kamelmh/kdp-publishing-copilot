# ══════════════════════════════════════════════════════════════════════════════
#  PATCH for entry_page.py — cross-platform Georgia registration
#
#  REPLACE these four lines near the top of entry_page.py:
#
#      pdfmetrics.registerFont(TTFont('Georgia', 'C:/Windows/Fonts/georgia.ttf'))
#      pdfmetrics.registerFont(TTFont('Georgia-Bold', 'C:/Windows/Fonts/georgiab.ttf'))
#      pdfmetrics.registerFont(TTFont('Georgia-Italic', 'C:/Windows/Fonts/georgiai.ttf'))
#      pdfmetrics.registerFont(TTFont('Georgia-BoldItalic', 'C:/Windows/Fonts/georgiaz.ttf'))
#
#  ...with the block below. Those absolute paths raise on macOS, Linux and CI,
#  so the module cannot even be imported off Windows. This searches the usual
#  locations per-OS and falls back to Gelasio (metric-compatible with Georgia,
#  OFL-licensed) so line breaks and text widths stay identical.
#
#  Drop the four Gelasio TTFs in a ./fonts folder beside entry_page.py to enable
#  the fallback. On your Windows machine real Georgia is found first and used.
# ══════════════════════════════════════════════════════════════════════════════

import os, glob as _glob
def _register_georgia()
