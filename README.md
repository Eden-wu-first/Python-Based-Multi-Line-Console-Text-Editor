# Python-Based Multi-Line Console Text Editor

**CSC1002: Computational Laboratory | Assignment 3**

This is a course project for **CSC1002: Computational Laboratory** at **CUHK-Shenzhen**. Please do not submit it as your own assignment.

A simple console-based multi-line text editor with Vim-like command operations, implemented in pure Python. It supports cursor movement, text editing, copy/paste, undo/redo, and display control, following the CSC1002 2025 assignment specifications.

---

## 📁 Project Files
| File Name | Description |
| ---- | ---- |
| main.py | Main Python source code of the editor |
| Editor-Multi-Line-Basic-2025.pdf | Official assignment requirements & specifications |
| test | Official tests examples |

---

## ✨ Core Features
- Vim-style single/double-letter command control
- Multi-line text editing & cursor positioning
- Row/line cursor display toggle
- Copy, paste, delete lines/words
- Undo & repeat last command
- Formatted console output with cursor highlighting

---

## 🚀 Quick Start
### Run the Editor
```bash
python main.py
```

### Command Format
- Most commands: single key (e.g. `h`, `j`, `x`)
- Insert/Append: `i[text]` / `a[text]` (e.g. `iHello` inserts text before cursor)
- Press Enter to execute each command

---

## 📌 Command Cheat Sheet
### Cursor Movement
| Command | Function |
| ---- | ---- |
| h | Move cursor left |
| j | Move cursor up |
| k | Move cursor down |
| l | Move cursor right |
| ^ | Jump to line start |
| $ | Jump to line end |
| w | Next word start |
| b | Previous word start |

### Text Editing
| Command | Function |
| ---- | ---- |
| i[text] | Insert text before cursor |
| a[text] | Append text after cursor |
| x | Delete character at cursor |
| dw | Delete word at cursor |
| dd | Delete current line |
| o | Insert empty line below |
| O | Insert empty line above |

### Copy & Paste
| Command | Function |
| ---- | ---- |
| yy | Copy current line |
| p | Paste below current line |
| P | Paste above current line |

### Control & Utility
| Command | Function |
| ---- | ---- |
| . | Toggle row cursor highlight |
| ; | Toggle line cursor marker (*) |
| u | Undo last command |
| r | Repeat last command |
| s | Show editor content |
| ? | Show help info |
| q | Quit program |

---

## 🧩 Development Rules
- Only `re` module is permitted
- Entire code in single Python file
- Functional programming only (no custom classes)
- Case-sensitive commands

---

## 📄 License
This project is open-sourced under the MIT License — you can freely use, modify and distribute it with copyright notice.

---

## 📝 Notes
This is a course assignment project for CSC1002 Computational Laboratory in CUHK-Shenzhen. All functions strictly follow the requirements in `Editor-Multi-Line-Basic-2025.pdf`.
