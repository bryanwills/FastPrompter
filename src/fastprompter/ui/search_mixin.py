"""Search mixin for FastPrompter — find/replace text functionality.

Extracted from main.py Phase 2b of the modularization plan.
Provides SearchMixin class for use as a mixin with FastPrompter QMainWindow.
"""

from PyQt6.QtGui import QTextCursor, QTextDocument
from PyQt6.QtWidgets import QMessageBox


class SearchMixin:
    """Mixin providing find/replace UI and logic.

    Type hints assume these attributes are provided by the FastPrompter
    QMainWindow instance at runtime:
        self.search_frame, self.replace_input, self.search_input,
        self.text_area, self.btn_replace, self.btn_replace_all
    """

    def show_find(self):
        """Show the find search bar."""
        self.search_frame.show()
        self.replace_input.hide()
        self.btn_replace.hide()
        self.btn_replace_all.hide()
        self.search_input.setFocus()
        self.search_input.selectAll()

    def show_replace(self):
        """Show the find/replace search bar."""
        self.search_frame.show()
        self.replace_input.show()
        self.btn_replace.show()
        self.btn_replace_all.show()
        self.search_input.setFocus()
        self.search_input.selectAll()

    def close_search(self):
        """Hide the search frame and return focus to text area."""
        self.search_frame.hide()
        self.text_area.setFocus()

    def find_next(self):
        """Find the next occurrence of search text."""
        self.find_text(backward=False)

    def find_prev(self):
        """Find the previous occurrence of search text."""
        self.find_text(backward=True)

    def find_text(self, backward=False):
        """Find text in the text area, wrapping around if needed."""
        text = self.search_input.text()
        if not text:
            return
        options = QTextDocument.FindFlag(0)
        if backward:
            options |= QTextDocument.FindFlag.FindBackward

        original_cursor = self.text_area.textCursor()
        found = self.text_area.find(text, options)

        if not found:
            cursor = self.text_area.textCursor()
            cursor.movePosition(
                QTextCursor.MoveOperation.End if backward else QTextCursor.MoveOperation.Start
            )
            self.text_area.setTextCursor(cursor)
            found_again = self.text_area.find(text, options)
            if not found_again:
                self.text_area.setTextCursor(original_cursor)

    def replace_text(self):
        """Replace the current selection with replace text, then find next."""
        cursor = self.text_area.textCursor()
        if cursor.hasSelection() and cursor.selectedText() == self.search_input.text():
            cursor.insertText(self.replace_input.text())
        self.find_next()

    def replace_all(self):
        """Replace all occurrences of search text with replace text."""
        search_str = self.search_input.text()
        if not search_str:
            return
        replace_str = self.replace_input.text()
        cursor = self.text_area.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.MoveOperation.Start)
        self.text_area.setTextCursor(cursor)
        count = 0
        while self.text_area.find(search_str):
            self.text_area.textCursor().insertText(replace_str)
            count += 1
        cursor.endEditBlock()
        QMessageBox.information(self, "Replace All", f"Replaced {count} occurrences.")

    def on_search_toggle(self, checked):
        """Toggle the sidebar search bar visibility."""
        self.search_bar.setVisible(checked)
        self.data["search_visible"] = str(checked)
        self.mark_dirty()
        if checked:
            self.search_bar.setFocus()
        else:
            self.search_bar.clear()
