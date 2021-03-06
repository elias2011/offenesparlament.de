from unicodedata import normalize as ucnorm, category

def normalize(text):
    """ Simplify a piece of text to generate a more canonical 
    representation. This involves lowercasing, stripping trailing
    spaces, removing symbols, diacritical marks (umlauts) and 
    converting all newlines etc. to single spaces.
    """
    if not isinstance(text, unicode):
        text = unicode(text)
    text = text.lower()
    decomposed = ucnorm('NFKD', text)
    filtered = []
    for char in decomposed:
        cat = category(char)
        if cat.startswith('C'):
            filtered.append(' ')
        elif cat.startswith('M'):
            # marks, such as umlauts
            continue
        elif cat.startswith('Z'):
            # newlines, non-breaking etc.
            filtered.append(' ')
        elif cat.startswith('S'):
            # symbols, such as currency
            continue
        else:
            filtered.append(char)
    text = u''.join(filtered)
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip()
    return ucnorm('NFKC', text)

def url_slug(text):
    text = normalize(text)
    text = text.replace(' ', '-')
    text = text.replace('/', '')
    text = text.replace('.', '-')
    text = text.replace('--', '-')
    text = text.strip('-')
    return text.lower()

def tokenize(text, splits='COPZ'):
    token = []
    for c in unicode(text):
        if category(c)[0] in splits:
            if len(token):
                yield u''.join(token)
            token = []
        else:
            token.append(c)
    if len(token):
        yield u''.join(token)

def speaker_name_transform(name):
    """ Convert a speaker name used in Web TV metadata to the more
    common format used in other locations. """
    cparts = name.split(',')
    if '(' in cparts[1]:
        cparts[1], pf = cparts[1].split(' (', 1)
        pf = pf.replace(')', '')
        cparts.append(pf)
    cparts[0], cparts[1] = cparts[1], cparts[0]
    fragment = " ".join(cparts)
    fragment.replace('(', '').replace(')', '')
    return fragment

def strip_control_characters(text):
    if not isinstance(text, basestring):
        return text
    _filtered = []
    for c in unicode(text):
        cat = category(c)[:1]
        if cat not in 'C':
            _filtered.append(c)
    return ''.join(_filtered)

