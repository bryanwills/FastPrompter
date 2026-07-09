"""Formatting mixin for FastPrompter — markdown rendering, text cleaning, and format clearing.

Extracted from main.py Phase 1 of the modularization plan.
Provides FormattingMixin class for use as a mixin with FastPrompter QMainWindow.
"""

import html
import re

import markdown
from PyQt6.QtGui import QFont, QTextCharFormat, QTextCursor

from fastprompter.core.logging import logger

# Pre-compiled regex patterns for markdown processing
_RE_DASH_LINE = re.compile(r"^\s*-{3,}\s*$")
_RE_HEADER_DASH = re.compile(r"^\s*-{3,}\s*$")
_RE_LIST_ITEM = re.compile(r"^\s*(?:[-*•+]\s|\d+\.\s)")
_RE_LIST_SUB = re.compile(r"^\s*[-*•+](?:\s+|$)|^\s*\d+\.\s+")
_RE_BOLD = re.compile(r"\*\*(.*?)\*\*")
_RE_ITALIC = re.compile(r"\*(?!\*)(.*?)\*")
_RE_INLINE_CODE = re.compile(r"`([^`]+)`")
_RE_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_RE_BULLET = re.compile(r"^\s*•")


class FormattingMixin:
    """Mixin providing markdown rendering, text cleaning, and format clearing.

    Type hints assume these attributes are provided by the FastPrompter
    QMainWindow instance at runtime:
        self.text_area, self.sound_manager, self._font_size,
        self._font_family, self._ui_scale
    """

    def apply_format(self, fmt_type):
        """Apply bold/italic/underline/strikethrough formatting to selection."""
        cursor = self.text_area.textCursor()
        cursor.beginEditBlock()
        fmt = cursor.charFormat()

        if fmt_type == "bold":
            fmt.setFontWeight(
                QFont.Weight.Bold if fmt.fontWeight() != QFont.Weight.Bold else QFont.Weight.Normal
            )
        elif fmt_type == "italic":
            fmt.setFontItalic(not fmt.fontItalic())
        elif fmt_type == "underline":
            fmt.setFontUnderline(not fmt.fontUnderline())
        elif fmt_type == "strike":
            fmt.setFontStrikeOut(not fmt.fontStrikeOut())

        cursor.mergeCharFormat(fmt)
        cursor.endEditBlock()
        self.text_area.setTextCursor(cursor)
        self.text_area.setFocus()
        self.mark_dirty()

    def toggle_header_line(self):
        """Ctrl+E: Toggle `# ` header + `**` bold markers (persists across sessions)."""
        cursor = self.text_area.textCursor()
        cursor.beginEditBlock()

        pos_in_block = cursor.positionInBlock()
        block = cursor.block()

        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
        sel = cursor.selectedText()

        # Remove old `**` if it happens to be there from the old version
        if sel.startswith("**") and sel.endswith("**") and len(sel) >= 4:
            sel = sel[2:-2]

        has_hdr = sel.startswith("# ")
        if has_hdr:
            new_text = sel[2:]
            offset = -2
        else:
            new_text = f"# {sel}"
            offset = 2

        cursor.insertText(new_text)

        # Apply visual format
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
        fmt = cursor.charFormat()
        if has_hdr:
            fmt.setFontWeight(QFont.Weight.Normal)
            fmt.setFontUnderline(False)
        else:
            fmt.setFontWeight(QFont.Weight.Bold)
            fmt.setFontUnderline(True)
        cursor.mergeCharFormat(fmt)

        cursor.endEditBlock()

        new_pos_in_block = max(0, pos_in_block + offset)
        new_cursor = self.text_area.textCursor()
        new_cursor.setPosition(block.position() + new_pos_in_block)
        self.text_area.setTextCursor(new_cursor)

        self.text_area.setFocus()
        self.mark_dirty()

    def apply_bold_smart(self):
        """Ctrl+B: Bold selected text. If nothing selected, bold/unbold entire current line."""
        cursor = self.text_area.textCursor()
        cursor.beginEditBlock()
        if not cursor.hasSelection():
            # Select whole current line
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
            cursor.movePosition(
                QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor
            )
            self.text_area.setTextCursor(cursor)
        self.apply_format("bold")
        cursor.endEditBlock()

    def toggle_bullet_conversion(self):
        """Toggle between bullet (•) and dash (-) list markers on selected text."""
        cursor = self.text_area.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            text = cursor.selectedText().replace("\u2029", "\n")
        else:
            text = self.text_area.toPlainText()
            cursor.select(QTextCursor.SelectionType.Document)

        lines = text.splitlines()
        if not lines:
            cursor.endEditBlock()
            return

        if any(_RE_BULLET.match(line) for line in lines):
            # Convert bullets back to dashes, skip divider lines
            new_lines = []
            for line in lines:
                if _RE_DASH_LINE.match(line):  # Protect --- dividers
                    new_lines.append(line)
                else:
                    new_lines.append(re.sub(r"^(\s*)•\s*", r"\1- ", line))
        else:
            # Convert dashes to bullets, skip divider lines (---)
            new_lines = []
            for line in lines:
                if _RE_DASH_LINE.match(line):  # Protect --- dividers from conversion
                    new_lines.append(line)
                else:
                    new_lines.append(re.sub(r"^(\s*)-\s+", r"\1• ", line))

        new_text = "\n".join(new_lines)
        cursor.insertText(new_text)
        cursor.endEditBlock()
        self.text_area.setFocus()
        self.mark_dirty()

    def insert_add_line(self):
        """Insert a horizontal markdown divider line (---) with smart spacing.

        If called mid-line or on a non-empty line, jumps to the end first.
        Inserts \n\n---\n\n and positions cursor on a fresh line ready to type.
        """
        cursor = self.text_area.textCursor()
        cursor.beginEditBlock()
        block = cursor.block()
        if cursor.positionInBlock() > 0 or block.text().strip():
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
        cursor.insertText("\n\n---\n\n")
        cursor.endEditBlock()
        self.text_area.setTextCursor(cursor)
        self.text_area.ensureCursorVisible()
        self.text_area.setFocus()
        self.mark_dirty()

    def simple_markdown_to_html(self, text):
        """Convert markdown text to styled HTML with fallback renderer."""


        try:
            # Full markdown renderer using standard Python markdown library if available
            body = markdown.markdown(html.escape(text), extensions=["fenced_code", "tables"])
        except Exception:
            # Fallback to simple regex renderer if markdown library not available
            lines = text.split("\n")
            html_lines = []
            in_code_block = False
            for line in lines:
                if line.startswith("```"):
                    if in_code_block:
                        html_lines.append("</pre>")
                        in_code_block = False
                    else:
                        html_lines.append(
                            "<pre style='background:#1a1a1a;padding:5px;border:1px solid #333'>"
                        )
                        in_code_block = True
                    continue
                if in_code_block:
                    html_lines.append(line.replace("<", "&lt;").replace(">", "&gt;"))
                    continue

                if line.startswith("### "):
                    html_lines.append(
                        f"<h3 style='color:#d4a842;margin:4px 0'>{html.escape(line[4:])}</h3>"
                    )
                elif line.startswith("## "):
                    html_lines.append(
                        f"<h2 style='color:#e0b856;margin:5px 0'>{html.escape(line[3:])}</h2>"
                    )
                elif line.startswith("# "):
                    html_lines.append(
                        f"<h1 style='color:#f0cc6a;margin:6px 0'>{html.escape(line[2:])}</h1>"
                    )
                elif line.startswith("> "):
                    html_lines.append(
                        f"<blockquote style='border-left:3px solid #7f848e;margin:4px 0;padding-left:8px;color:#7f848e'><i>{html.escape(line[2:])}</i></blockquote>"
                    )
                elif _RE_HEADER_DASH.match(line):
                    html_lines.append("<hr style='border:1px solid #5a4a2a;'>")
                elif _RE_LIST_ITEM.match(line):
                    content = _RE_LIST_SUB.sub("", line)
                    content = html.escape(content)
                    content = _RE_BOLD.sub(r"<b>\1</b>", content)
                    content = _RE_ITALIC.sub(r"<i>\1</i>", content)
                    content = _RE_INLINE_CODE.sub(
                        r'<code style="background:#1a1a1a;padding:0 2px;color:#e06c75">\1</code>',
                        content,
                    )
                    content = _RE_LINK.sub(r'<a href="\2" style="color:#61afef">\1</a>', content)
                    html_lines.append(f"<li style='margin:1px 0'>{content}</li>")
                else:
                    line_text = line
                    line_text = html.escape(line_text)
                    line_text = _RE_BOLD.sub(r"<b>\1</b>", line_text)
                    line_text = _RE_ITALIC.sub(r"<i>\1</i>", line_text)
                    line_text = _RE_INLINE_CODE.sub(
                        r'<code style="background:#1a1a1a;padding:0 2px;color:#e06c75">\1</code>',
                        line_text,
                    )
                    line_text = _RE_LINK.sub(
                        r'<a href="\2" style="color:#61afef">\1</a>',
                        line_text,
                    )
                    html_lines.append(
                        f"<p style='margin:1px 0'>{line_text}</p>" if line_text.strip() else "<br>"
                    )
            body = "\n".join(html_lines)

        return f"<html><body style='color:#c4ba9f;background:#0f0f0f;font-family:Verdana,sans-serif;font-size:11px;padding:6px'>{body}</body></html>"

    def clean_excessive_newlines(self):
        """Remove excessive empty lines, preserving dashes."""
        self.add_data_undo_state("Clean newlines")
        self.sound_manager.play("clear")
        try:
            text = self.text_area.toPlainText()
            if not text:
                return
            lines = text.split("\n")
            is_empty = [bool(not line.strip()) for line in lines]
            is_dash = [bool(_RE_DASH_LINE.match(line)) for line in lines]

            out = []
            i = 0
            while i < len(lines):
                if not is_empty[i]:
                    out.append(lines[i])
                    i += 1
                else:
                    j = i
                    while j < len(lines) and is_empty[j]:
                        j += 1
                    prev_is_dash = i > 0 and is_dash[i - 1]
                    next_is_dash = j < len(lines) and is_dash[j]

                    if prev_is_dash or next_is_dash:
                        out.extend(lines[i:j])
                    else:
                        num_to_keep = min(1, j - i)
                        out.extend(lines[i : i + num_to_keep])
                    i = j

            cleaned_text = "\n".join(out)
            if cleaned_text != text:
                cursor = self.text_area.textCursor()
                cursor.beginEditBlock()
                cursor.select(QTextCursor.SelectionType.Document)
                cursor.insertText(cleaned_text)
                cursor.endEditBlock()
        except Exception:
            logger.exception("Failed to clean excessive newlines")

    def clear_formatting(self):
        """Reset text formatting to base font with plain style."""
        self.sound_manager.play("clear")
        cursor = self.text_area.textCursor()
        cursor.beginEditBlock()

        clean_format = QTextCharFormat()
        try:
            base_size = self._font_size
        except Exception:
            base_size = 11
        font_name = self._font_family
        try:
            scale = self._ui_scale
        except Exception:
            scale = 1.0
        font_size = max(8, int(round(base_size * scale)))
        font = QFont(font_name, font_size)
        font.setStyleStrategy(
            QFont.StyleStrategy(
                int(QFont.StyleStrategy.NoAntialias.value)
                | int(QFont.StyleStrategy.NoSubpixelAntialias.value)
            )
        )
        clean_format.setFont(font)
        clean_format.setFontWeight(QFont.Weight.Normal)
        clean_format.setFontItalic(False)
        clean_format.setFontUnderline(False)
        clean_format.setFontStrikeOut(False)

        try:
            if cursor.hasSelection():
                raw_text = cursor.selectedText().replace("\u2029", "\n")
                cursor.insertText(raw_text, clean_format)
            else:
                raw_text = self.text_area.toPlainText()
                self._set_plain_text_clean(self.text_area, raw_text)
                cursor = self.text_area.textCursor()
                cursor.select(QTextCursor.SelectionType.Document)
                cursor.setCharFormat(clean_format)
                cursor.clearSelection()
                self.text_area.setTextCursor(cursor)
        finally:
            cursor.endEditBlock()
            self.text_area.blockSignals(False)

        self.apply_font()
        self.mark_dirty()
        self.cache_current_text()
