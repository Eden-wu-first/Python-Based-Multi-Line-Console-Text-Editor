import re

# global variables
cmd_buf = []             # command buffer
undo_buf = []            # undo buffer
last_cmd = None          # last command
row_cursor_on = False    # row cursor display flag
line_cursor_on = False   # line cursor display flag
copy_buffer = None       # copy buffer
copy_buf_history = []    # copy buffer history


def display_help_info() -> None:
    '''
    Display this help info.

    Args:
        None.
    
    Returns:
        None.
    '''
    print(
        '? - display this help info\n'
        '. - toggle row cursor on and off\n'
        '; - toggle line cursor on and off\n'
        'h - move cursor left\n'
        'j - move cursor up\n'
        'k - move cursor down\n'
        'l - move cursor right\n'
        '^ - move cursor to beginning of the line\n'
        '$ - move cursor to end of the line\n'
        'w - move cursor to beginning of next word\n'
        'b - move cursor to beginning of previous word\n'
        'i - insert <text> before cursor\n'
        'a - append <text> after cursor\n'
        'x - delete character at cursor\n'
        'dw - delete word and trailing spaces at cursor\n'
        'yy - copy current line to memory\n'
        'p - paste copied line(s) below line cursor\n'
        'P - paste copied line(s) above line cursor\n'
        'dd - delete line\n'
        'o - insert empty line below\n'
        'O - insert empty line above\n'
        'u - undo previous command\n'
        'r - repeat last command\n'
        's - show content\n'
        'q - quit program'
    )


def toggle_row_cursor() -> None:
    '''
    Toggle row cursor on and off.

    Args:
        None.

    Returns:
        None.
    '''
    global row_cursor_on
    row_cursor_on = not row_cursor_on


def toggle_line_cursor() -> None:
    '''
    Toggle line cursor on and off.

    Args:
        None.

    Returns:
        None.
    '''
    global line_cursor_on
    line_cursor_on = not line_cursor_on


def format_display(lines:list, current_line:int, cursor:int) -> None:
    '''
    Display the content in a formatted way.

    Args:
        lines (list): List of lines to display.
        current_line (int): Current line number.
        cursor (int): Cursor position.
    
    Returns:
        None.
    '''
    if not lines:
        return  # No content to display
    for i, line in enumerate(lines):
        if line_cursor_on:
            prefix = '*' if i == current_line else ' '
        else:
            prefix = ''
        if i == current_line:
            if row_cursor_on and line:
                pos = min(cursor, len(line) - 1)
                content = line[:pos] + "\033[42m" + line[pos] + "\033[0m" + line[pos + 1:]
            else:
                content = line
        else:
            content = line
        print(prefix + content)


def move_cursor_left(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Move cursor left.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content:
        return content, line_cur, row_cur
    return content, line_cur, max(0, row_cur - 1)


def move_cursor_up(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Move cursor up.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    
    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content:
        return content, line_cur, row_cur
    line_cur = max(0, line_cur - 1)
    return content, line_cur, min(row_cur + 1, (len(content[line_cur]) - 1) if content[line_cur] else 0)


def move_cursor_down(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Move cursor down.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content:
        return content, line_cur, row_cur
    line_cur = min(len(content) - 1, line_cur + 1)
    return content, line_cur, min(row_cur, (len(content[line_cur]) - 1) if content[line_cur] else 0)


def move_cursor_right(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Move cursor right.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    
    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content or not content[line_cur]:
        return content, line_cur, row_cur
    return content, line_cur, min(len(content[line_cur]) - 1, row_cur + 1) if content[line_cur] else 0


def move_cursor_beginning(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Move cursor to the beginning of the line.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    
    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content:
        return content, line_cur, row_cur
    return content, line_cur, 0


def move_cursor_end(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Move cursor to the end of the line.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content or not content[line_cur]:
        return content, line_cur, row_cur
    return content, line_cur, len(content[line_cur]) - 1 if content[line_cur] else 0


def move_cursor_next(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Move cursor to the next character.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content or not content[line_cur]:
        return content, line_cur, row_cur
    line = content[line_cur]
    while row_cur < len(line) - 1 and not line[row_cur].isspace():
        row_cur += 1
    while row_cur < len(line) - 1 and line[row_cur].isspace():
        row_cur += 1
    return content, line_cur, row_cur


def move_cursor_previous(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Move cursor to the previous character.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content or not content[line_cur] or row_cur == 0:
        return content, line_cur, row_cur
    line = content[line_cur]
    regex = r"\S*$" if re.match(r"\S", line[row_cur - 1]) else r"\S+\W*$"
    match = re.search(regex, line[:row_cur])
    if match:
        row_cur = match.start()
    return content, line_cur, row_cur


def insert_text(content:list, line_cur:int, row_cur:int, text:str) -> tuple:
    '''
    Insert text at the cursor position.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
        text (str): Text to insert.
    
    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content:
        content.append("")
        line_cur = 0
        row_cur = 0
    if text.isspace():
        # Verify whether the text is a space
        return content, line_cur, row_cur
    else:
        content[line_cur] = content[line_cur][:row_cur] + text + content[line_cur][row_cur:]
        return content, line_cur, row_cur


def append_text(content:list, line_cur:int, row_cur:int, text:str) -> tuple:
    '''
    Append text at the end of the line.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
        text (str): Text to append.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content:
        content.append("")
        line_cur = 0
        row_cur = -1
    row_cur += 1
    content[line_cur] = content[line_cur][:row_cur + 1] + text + content[line_cur][row_cur + 1:]
    row_cur = min(row_cur + len(text), len(content[line_cur]) - 1)
    return content, line_cur, row_cur


def delete_character(content:list, line_cur:str, row_cur:str) -> tuple:
    '''
    Delete the character at the cursor position.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    # verify the cursor
    if not content:
        return content, line_cur, row_cur
    if row_cur >= len(content[line_cur]):
        row_cur = len(content[line_cur]) - 1
    else:
        content[line_cur] = content[line_cur][:row_cur] + content[line_cur][row_cur + 1:]
    return content, line_cur, row_cur


def delete_word(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Delete the word at the cursor position.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content:
        return content, line_cur, row_cur
    if content[line_cur]:
        match = re.match(r"\S+\s*|\s+", content[line_cur][row_cur:])
        if match:
            end = row_cur + match.end()
            content[line_cur] = content[line_cur][:row_cur] + content[line_cur][end:]
            row_cur = min(row_cur, len(content[line_cur]) - 1 if content[line_cur] else 0)
    return content, line_cur, row_cur


def copy_line(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Copy the current line to the clipboard.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    global copy_buffer, copy_buf_history
    if len(content) == 0:
        return content, line_cur, row_cur  # nothing to copy
    if copy_buffer is not None:
        copy_buf_history.append(copy_buffer)
    else:
        copy_buf_history.append("")
    copy_buffer = content[line_cur]
    return content, line_cur, row_cur


def paste_line_below(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Paste the current line below the current line.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    global copy_buffer
    if copy_buffer is not None:
        content.insert(line_cur + 1, copy_buffer)
        line_cur += 1
        row_cur = min(row_cur, len(content[line_cur]) - 1 if content[line_cur] else 0)
    return content, line_cur, row_cur


def paste_line_above(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Paste the current line above the current line.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    global copy_buffer
    if copy_buffer is not None:
        content.insert(line_cur, copy_buffer)
        row_cur = min(row_cur, len(content[line_cur]) - 1 if content[line_cur] else 0)
    return content, line_cur, row_cur


def delete_line(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Delete the current line.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if not content:
        return content, line_cur, row_cur
    content.pop(line_cur)
    if not content:
        return [], 0, 0
    line_cur = max(line_cur - 1, 0) if line_cur >= len(content) else line_cur
    row_cur = min(row_cur, len(content[line_cur]) - 1 if content[line_cur] else 0)
    return content, line_cur, row_cur


def insert_empty_line_below(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Insert an empty line below the current line.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    content.insert(line_cur + 1, "")
    return content, line_cur + 1, 0


def insert_empty_line_above(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Insert an empty line above the current line.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    
    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    content.insert(line_cur, "")
    return content, line_cur, 0


def undo(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Undo the last command.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    global undo_buf, cmd_buf, last_cmd, copy_buffer, copy_buf_history
    if last_cmd == ".":
        toggle_row_cursor()
    elif last_cmd == ";":
        toggle_line_cursor()
    if undo_buf:
        prev_content, prev_line_cur, prev_row_cur = undo_buf.pop()
        # Restore previous state
        content = list(prev_content)
        line_cur = prev_line_cur
        row_cur = prev_row_cur
        if last_cmd == "yy" and copy_buf_history:
            copy_buffer = copy_buf_history.pop()
        elif last_cmd == "yy":
            copy_buffer = None
        if cmd_buf:
            cmd_buf.pop()
        last_cmd = cmd_buf[-1] if cmd_buf else None
    return content, line_cur, row_cur


def repeat(content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Repeat the last command.

    Args:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    if last_cmd:
        content, line_cur, row_cur = parse_command(last_cmd, content, line_cur, row_cur)
    return content, line_cur, row_cur


valid_commands = {
    "?": display_help_info,
    ".": toggle_row_cursor,
    ";": toggle_line_cursor,
    "h": move_cursor_left,
    "j": move_cursor_up,
    "k": move_cursor_down,
    "l": move_cursor_right,
    "^": move_cursor_beginning,
    "$": move_cursor_end,
    "w": move_cursor_next,
    "b": move_cursor_previous,
    "i": insert_text,
    "a": append_text,
    "x": delete_character,
    "dw": delete_word,
    "yy": copy_line,
    "p": paste_line_below,
    "P": paste_line_above,
    "dd": delete_line,
    "o": insert_empty_line_below,
    "O": insert_empty_line_above,
    "u": undo,
    "r": repeat,
    "s": None,
    "q": exit
}


def is_valid_command(cmd:str) -> bool:
    '''
    Check if the command is valid.

    Args:
        cmd (str): Command to check.

    Returns:
        bool: True if the command is valid, False otherwise.
    '''
    if cmd[0] in "ai":
        return len(cmd) > 1
    return cmd in valid_commands


def parse_command(cmd:str, content:list, line_cur:int, row_cur:int) -> tuple:
    '''
    Parse the command and execute it.

    Args:
        cmd (str): Command to execute.
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.

    Returns:
        content (list): Content to display.
        line_cur (int): Current line number.
        row_cur (int): Current row number.
    '''
    global last_cmd, cmd_buf
    if cmd[0] in "ai":
        content, line_cur, row_cur = valid_commands[cmd[0]](content, line_cur, row_cur, cmd[1:])
    elif cmd in ".;?q":
        valid_commands[cmd]()
    elif cmd == "s":
        pass
    else:
        content, line_cur, row_cur = valid_commands[cmd](content, line_cur, row_cur)
    if cmd not in ("u", "r", "?"):
        cmd_buf.append(cmd)
        last_cmd = cmd
    return content, line_cur, row_cur


def main():
    content = []
    line_cur, row_cur = 0, 0
    while True:
        cmd = input(">")
        if not cmd or not is_valid_command(cmd):
            continue
        if cmd not in ("u", "?"):
            undo_buf.append((list(content), line_cur, row_cur))
        content, line_cur, row_cur = parse_command(cmd, content, line_cur, row_cur)
        if cmd != "?":
            format_display(content, line_cur, row_cur)


if __name__ == "__main__":
    main()