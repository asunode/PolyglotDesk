"""Giriş noktası: python3 -m cevirmen"""

import sys

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from .arayuz import AnaPencere


def _acik_palet() -> QPalette:
    # Referans tasarım açık renkli; sistem koyu temada olsa da aynı görünsün.
    palet = QPalette()
    for rol, renk in (
        (QPalette.ColorRole.Window, "#f4f4f4"), (QPalette.ColorRole.WindowText, "#202124"),
        (QPalette.ColorRole.Base, "#ffffff"), (QPalette.ColorRole.AlternateBase, "#f8f9fa"),
        (QPalette.ColorRole.Text, "#202124"), (QPalette.ColorRole.Button, "#ffffff"),
        (QPalette.ColorRole.ButtonText, "#202124"), (QPalette.ColorRole.Highlight, "#1a73e8"),
        (QPalette.ColorRole.HighlightedText, "#ffffff"), (QPalette.ColorRole.ToolTipBase, "#ffffff"),
        (QPalette.ColorRole.ToolTipText, "#202124"), (QPalette.ColorRole.PlaceholderText, "#70757a"),
    ):
        palet.setColor(rol, QColor(renk))
    return palet


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("PolyglotDesk")
    app.setDesktopFileName("cevirmen")
    app.setStyle("Fusion")
    app.setPalette(_acik_palet())
    ceviri = QTranslator(app)
    if ceviri.load(QLocale("tr_TR"), "qtbase", "_", QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)):
        app.installTranslator(ceviri)
    pencere = AnaPencere()
    pencere.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
