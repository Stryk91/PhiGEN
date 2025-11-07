from __future__ import annotations

import sys
import os
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtUiTools import QUiLoader


def dark_neon_palette(app: QtWidgets.QApplication) -> None:
    # Basic dark palette to roughly match the Tk app
    palette = QtGui.QPalette()
    bg = QtGui.QColor("#0a0a0a")
    surface = QtGui.QColor("#111111")
    text = QtGui.QColor("#e6e6e6")
    accent = QtGui.QColor("#39ff14")

    palette.setColor(QtGui.QPalette.Window, bg)
    palette.setColor(QtGui.QPalette.WindowText, text)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#0f0f0f"))
    palette.setColor(QtGui.QPalette.AlternateBase, surface)
    palette.setColor(QtGui.QPalette.ToolTipBase, surface)
    palette.setColor(QtGui.QPalette.ToolTipText, text)
    palette.setColor(QtGui.QPalette.Text, text)
    palette.setColor(QtGui.QPalette.Button, surface)
    palette.setColor(QtGui.QPalette.ButtonText, text)
    palette.setColor(QtGui.QPalette.BrightText, accent)
    palette.setColor(QtGui.QPalette.Highlight, accent)
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#000000"))

    app.setPalette(palette)

    # Flat icon-only buttons look better without borders; a light style sheet
    app.setStyleSheet(
        """
        QWidget { background-color: #0a0a0a; color: #e6e6e6; }
        QLineEdit, QSpinBox { background-color: #0f0f0f; color: #e6e6e6; border: 1px solid #222; padding: 4px; }
        QPushButton { background-color: #111111; border: 1px solid #222; padding: 6px 10px; }
        QListWidget { background-color: #0f0f0f; color: #e6e6e6; border: 1px solid #222; }
        QStatusBar { background-color: #0a0a0a; color: #9aa0a6; }
        """
    )


def load_ui(path: Path) -> QtWidgets.QWidget:
    # Ensure absolute path and set loader working directory for relative resources
    abs_path = Path(path).resolve()
    if not abs_path.exists():
        raise RuntimeError(f"UI file not found: {abs_path}")

    loader = QUiLoader()
    try:
        # Make resources like ../TEMPSVG/* resolve relative to the .ui file location
        fi = QtCore.QFileInfo(str(abs_path))
        loader.setWorkingDirectory(fi.dir())
    except Exception:
        pass

    ui_file = QtCore.QFile(str(abs_path))
    if not ui_file.open(QtCore.QIODevice.ReadOnly):
        raise RuntimeError(f"Failed to open UI file: {abs_path}")
    try:
        try:
            widget = loader.load(ui_file)
        except Exception as e:
            # First attempt failed — try a QBuffer-based fallback, then rethrow with diagnostics.
            try:
                ui_file.seek(0)
                data = ui_file.readAll()
                buf = QtCore.QBuffer()
                buf.setData(data)
                buf.open(QtCore.QIODevice.ReadOnly)
                try:
                    widget = loader.load(buf)
                finally:
                    buf.close()
            except Exception:
                widget = None
            if widget is None:
                # Enhance diagnostics with loader errorString and working dir
                try:
                    err = loader.errorString()
                except Exception:
                    err = ""
                cwd = os.getcwd()
                raise RuntimeError(
                    f"QUiLoader.load() failed for {abs_path}: {e}\n"
                    f"loader.errorString(): {err}\n"
                    f"cwd: {cwd}\n"
                    f"ui exists: {abs_path.exists()} size: {abs_path.stat().st_size if abs_path.exists() else 'n/a'}"
                ) from e
        if widget is None:
            # Final fallback: try loading through a new QUiLoader instance using QBuffer
            try:
                ui_file.seek(0)
                data = ui_file.readAll()
                buf = QtCore.QBuffer()
                buf.setData(data)
                buf.open(QtCore.QIODevice.ReadOnly)
                loader2 = QUiLoader()
                try:
                    fi = QtCore.QFileInfo(str(abs_path))
                    loader2.setWorkingDirectory(fi.dir())
                except Exception:
                    pass
                try:
                    widget = loader2.load(buf)
                finally:
                    buf.close()
            except Exception:
                widget = None
        if widget is None:
            try:
                err = loader.errorString()
            except Exception:
                err = ""
            raise RuntimeError(f"Failed to load UI: {abs_path}\nloader.errorString(): {err}")
        return widget
    finally:
        ui_file.close()


def main(argv: list[str]) -> int:
    app = QtWidgets.QApplication(argv)
    dark_neon_palette(app)

    # Ensure working directory is project root so relative paths in .ui work
    try:
        proj_root = Path(__file__).resolve().parent
        os.chdir(str(proj_root))
    except Exception:
        pass

    ui_path = Path(__file__).with_name("ui") / "password_vault.ui"
    window = load_ui(ui_path)

    # Try to limit form width similar to Tk app: cap roughly at ~640px when window is 1200px wide.
    # If the widget names change in Designer, update these names accordingly.
    form_container = window.findChild(QtWidgets.QWidget, "formContainer")
    if form_container is not None:
        # Use a layout stretcher to center and bound width
        outer = QtWidgets.QHBoxLayout()
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        parent_layout = window.findChild(QtWidgets.QVBoxLayout, "verticalLayout")
        if parent_layout is not None:
            # Remove and reinsert form_container wrapped in centering layout
            index = parent_layout.indexOf(form_container)
            if index != -1:
                parent_layout.takeAt(index)
                center_wrap = QtWidgets.QWidget(window)
                center_layout = QtWidgets.QHBoxLayout(center_wrap)
                center_layout.setContentsMargins(0, 0, 0, 0)
                center_layout.addStretch(1)
                form_container.setMaximumWidth(640)  # default cap; user can adjust in Designer
                center_layout.addWidget(form_container)
                center_layout.addStretch(1)
                parent_layout.insertWidget(index, center_wrap)

    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
