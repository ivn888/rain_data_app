def as_ansi_escape(values):
    return f'\x1b[{values}m'

ANSI_COLORS = {
    'success': as_ansi_escape('6;30;42'),
    'about': as_ansi_escape('6;30;44'),
    'process': as_ansi_escape('0;30;47'),
    'happening': as_ansi_escape('1;33;40'),
    'attention': as_ansi_escape('1;37;45'),
    'stop':  as_ansi_escape('0')
}

def wrap_color(color, string):
    return ANSI_COLORS[color] + string + ANSI_COLORS['stop']
