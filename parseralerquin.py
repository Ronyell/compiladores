import ox
from data import Data

lexer = ox.make_lexer([
    ('EQUAL', r'='),
    ('STRING', r'\"'),
    ('TEXT', r'[\w*°*\?*\(*\)*\.*\,*\:*\-*]+'),
    ('OPEN_SECTION', r'\['),
    ('CLOSE_SECTION', r'\]'),
    ('OPEN_SUBSECTION', r'\[\['),
    ('CLOSE_SUBSECTION', r'\]\]'),
    ('OPEN_DATA', r'\{'),
    ('CLOSE_DATA', r'\}'),
    ('IGNORE', r'\s+'),
    ('COMMENT', r'\#'),
])

tokens_list = ['EQUAL',
               'STRING',
               'TEXT',
               'OPEN_SECTION',
               'CLOSE_SECTION',
               'OPEN_SUBSECTION',
               'CLOSE_SUBSECTION',
               'OPEN_DATA',
               'CLOSE_DATA',
               'IGNORE',
               'COMMENT']

all_body_ignore = lambda ignore, all_file: (all_file)
all_body= lambda left, right: (left, right)
open_close = lambda open, text, close: (text)
section = lambda open, text, close, end_line, body: (('section',text), body)
section_no_body = lambda open, text, close, end_line: (('section',text))
subsection = lambda open, text, close,end_line, body: (('subsection',text), body)
open_close_ignore = lambda open, ignoreopen, text, ignoreclose, close: (text)
open_close_data_ignore = lambda open_data, ignoreopen, text, ignoreclose, close_data: (('open_data',open_data),text,('close_data',close_data))
data_compound = lambda left, ignore, right:(left, right)
string_data = lambda left, data, right: (('open_string',left), data, ('close_string',right))
data_ignore = lambda left, ignore,right: (left, right)
data_comment = lambda hash_comment, comment: (('comment',hash_comment), comment)
data_comment_hash = lambda hash_comment: ('comment',hash_comment)
data= lambda left, right: (left, right)
attribute = lambda variable, equal, attribute, end_line: (variable,('attr', equal), attribute)
atom = lambda text: ('text',text)

parser = ox.make_parser([
    ('all_file : IGNORE all_file', all_body_ignore),
    ('all_file : comment IGNORE all_file', data_ignore),
    ('all_file : all_section', lambda x:x),
    ('all_section : all_section section', all_body),
    ('all_section : section', lambda x:x),
    ('section : OPEN_SECTION TEXT CLOSE_SECTION IGNORE body_section', section),
    ('section : OPEN_SECTION TEXT CLOSE_SECTION IGNORE', section_no_body),
    ('body_section : body_section subsection', all_body),
    ('body_section : subsection', lambda x:x),
    ('body_section : body', lambda x:x),
    ('subsection : OPEN_SUBSECTION TEXT CLOSE_SUBSECTION IGNORE body', subsection),
    ('body : body attribute', all_body),
    ('body : attribute', lambda x:x),
    ('attribute : comment IGNORE attribute', data_ignore),
    ('attribute : atom EQUAL data_compound IGNORE', attribute),
    ('data_compound : OPEN_DATA IGNORE data_ignore IGNORE CLOSE_DATA', open_close_data_ignore),
    ('data_ignore : data_ignore IGNORE data_compound', data_ignore),
    ('data_ignore : data_compound', lambda x:x),
    ('data_compound : STRING data STRING', string_data),
    ('data_compound : data', lambda x: x),
    ('comment : COMMENT data', data_comment),
    ('data : data atom', data),
    ('data : atom', lambda x: x),
    ('atom : TEXT', atom),
], tokens_list)

data = Data()
expr = data.return_data()


def extract_head_type(head):
    if head is 'section':
        return 'section'
    elif head is 'subsection':
        return 'subsection'
    elif head is 'open_data':
        return 'open_data'
    elif head is 'close_data':
        return 'close_data'
    elif head is 'text':
        return 'text'
    elif head is 'comment':
        return 'comment'
    elif head is 'attr':
        return 'attr'
    elif head is 'open_string':
        return 'open_string'
    elif head is 'close_string':
        return 'close_string'
    else:
        return None


def eval(ast):
    head, *tail = ast
    string = ''
    if head:
        type_node = extract_head_type(head)
        if type_node:
            return type_node
        elif not type_node:
            type_node = eval(head)
            if type_node == 'comment':
                print(extract_comment(tail))
    if tail:
        eval(tail)


def extract_comment(data):
    head, *tail = data
    string = ''
    if head is 'text':
        return tail[0] + ' '
    elif head:
        string += extract_comment(head)
    if tail:
        string += extract_comment(tail)
    if not head and not tail:
        string += '\n'

    return string


def extract_data(data):
    head, *tail = data
    string = ''
    if head is 'text' or head is 'open_string' or head is 'close_string':
        return tail[0] + ' '
    elif head is 'close_data':
        string += '\n'
    else:
        if head:
            string += extract_data(head)
        if tail:
            string += extract_data(tail)

    return string


def extract_section(data):
    head, *tail = data
    string = ''
    if head is 'section' or head is 'open_string' or head is 'close_string':
        return tail[0] + ' '
    elif head is 'close_data':
        string += '\n'
    else:
        if head:
            string += extract_data(head)
        if tail:
            string += extract_data(tail)

    return string


tokens = lexer(expr)
ast = parser(tokens)
eval(ast)
