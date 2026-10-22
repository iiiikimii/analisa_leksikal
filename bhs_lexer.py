
class Lexer:
    KEYWORDS = [
        'cetak',
        'ataujika',
        'jika',
        'selain',
        'lainnya',
        'selama',
        'untuk',
        'akhir',
        'else',
        'if',
        'while',
        'for'
    ]

    OPERATORS = ['=', '+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=']
    SYMBOLS = ['(', ')', ':']

    def __init__(self, code):
        self.code = code
        self.line_nr = 0
        self.returned_token = None
        self.token_feed = self.tokens()

    def raise_error(self, msg):
        raise ValueError(f"Baris {self.line_nr}: {msg}")

    def tokens(self):
        for line in self.code.splitlines():
            self.line_nr += 1
            line = line.strip()

            # TODO 2: Baris kosong
            if not line:
                yield ('NEWLINE',)
                continue

            i = 0
            tokens = []

            while i < len(line):
                ch = line[i]

                # TODO 3: Abaikan spasi dan tab
                if ch.isspace():
                    i += 1
                    continue

                # TODO 4: String
                if ch == "'" or ch == '"':
                    quote = ch
                    i += 1
                    start = i

                    while i < len(line) and line[i] != quote:
                        i += 1

                    if i >= len(line):
                        self.raise_error("String tidak ditutup")

                    tokens.append(('STRING', line[start:i]))
                    i += 1
                    continue

                # TODO 5: Operator dan simbol
                two_char = line[i:i + 2]

                if two_char in ('==', '!=', '<=', '>='):
                    tokens.append(two_char)
                    i += 2
                    continue

                if ch in self.OPERATORS or ch in self.SYMBOLS:
                    tokens.append(ch)
                    i += 1
                    continue

                # TODO 6: Angka
                if ch.isdigit() or (
                    ch == '.'
                    and i + 1 < len(line)
                    and line[i + 1].isdigit()
                ):
                    start = i
                    dot_count = 0

                    while i < len(line):
                        if line[i].isdigit():
                            i += 1
                        elif line[i] == '.':
                            if dot_count == 1:
                                self.raise_error(
                                    "Format angka tidak sah"
                                )
                            dot_count += 1
                            i += 1
                        else:
                            break

                    tokens.append(line[start:i])
                    continue

                # TODO 7: Identifier dan keyword
                if ch.isalpha() or ch == '_':
                    start = i

                    while i < len(line) and (
                        line[i].isalnum() or line[i] == '_'
                    ):
                        i += 1

                    tokens.append(line[start:i])
                    continue

                # TODO 8: Karakter tidak dikenal
                self.raise_error(f"Token tidak sah: {ch}")

            # TODO 9: Klasifikasi token
            for t in tokens:
                if isinstance(t, tuple):
                    yield t
                elif t in self.KEYWORDS:
                    yield ('KEYWORD', t)
                elif t in self.OPERATORS:
                    yield ('OPERATOR', t)
                elif t in self.SYMBOLS:
                    yield ('SYMBOL', t)
                else:
                    try:
                        if '.' in t:
                            yield ('NUMBER', float(t))
                        else:
                            yield ('NUMBER', int(t))
                    except ValueError:
                        yield ('IDENTIFIER', t)

            yield ('NEWLINE',)

    def next_token(self):
        if self.returned_token is not None:
            tok = self.returned_token
            self.returned_token = None
            return tok

        try:
            return next(self.token_feed)
        except StopIteration:
            return None

    def return_token(self, tok):
        if tok is not None:
            self.returned_token = tok

    def reset_tokenizer(self):
        self.line_nr = 0
        self.returned_token = None
        self.token_feed = self.tokens()
