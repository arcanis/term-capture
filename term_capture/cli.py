import os
import pty
import pyperclip
import pyte
import re
import sys
import time

shell = ('/bin/bash', '--rcfile', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'init.sh'))

def main():
    buffer = bytearray()

    def master_read(fd):
        nonlocal buffer
        data = os.read(fd, 1024)
        buffer += data
        return data

    def stdin_read(fd):
        data = os.read(fd, 1024)
        return data

    os.environ['PS1'] = r'\[\e[32m\]❯\[\e[m\] \[\e[94m\]/home/project\[\e[m\] \[\e[32m\]❯\[\e[m\] '
    os.environ['PROMPT_COMMAND'] = 'export PROMPT_COMMAND=echo'

    pty.spawn(shell, master_read, stdin_read)

    screen_width = 300
    screen_height = 80

    screen = pyte.Screen(screen_width, screen_height)
    stream = pyte.Stream(screen)
    
    buffer_str = bytes(buffer).decode('utf8')
    buffer_str = re.sub(r'[^\n]* exit(\r\n|[\r\n])$', '', buffer_str)

    stream.feed(buffer_str)

    output = ""
    span_open = False

    current_fg = 'default'
    current_bg = 'default'
    current_bold = False

    def is_hex_color(val):
        return re.match(r'^[a-f0-9]{6}$', val)

    def update_span():
        nonlocal output, span_open

        output += '</span>' if span_open else ''
        span_open = False

        classes = []
        styles = []

        if current_fg != 'default':
            if is_hex_color(current_fg):
                styles.append('color: #%s' % current_fg)
            else:
                classes.append('term-fg-%s' % current_fg)

        if current_bg != 'default':
            if is_hex_color(current_bg):
                styles.append('background-color: #%s' % current_bg)
            else:
                classes.append('term-bg-%s' % current_bg)

        if current_bold:
            classes.append('term-bold')

        if len(classes) > 0 or len(styles) > 0:
            output += '<span'

            if len(classes) > 0:
                output += ' class="%s"' % ' '.join(classes)
            if len(styles) > 0:
                output += ' style="%s"' % '; '.join(styles)

            output += '>'
            span_open = True

    for y in range(0, screen_height):
        for x in range(0, screen_width):
            char = screen.buffer[y][x]

            needs_update = False
            if char.fg != current_fg:
                current_fg = char.fg
                needs_update = True
            if char.bg != current_bg:
                current_bg = char.bg
                needs_update = True
            if char.bold != current_bold:
                current_bold = char.bold
                needs_update = True

            if needs_update:
                update_span()

            output += char.data

        output += '\n'

    output = re.sub(r' +\n', r'\n', output)
    output = output.rstrip()

    output += '</span>' if span_open else ''
    output = '<div class="term"><div class="term-header"></div><div class="term-body">%s</div></div>\n' % output

    pyperclip.copy(output)

    print()
    print('The HTML terminal output is now in your clipboard')

if __name__ == '__main__':
    main()
