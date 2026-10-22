# =============================================================
# BAHASAKU - PROGRAM UTAMA
# =============================================================

import sys

from bhs_lexer import Lexer

class bahasaKu:
    def __init__(self, code):
        self.code = code

    def run(self):
 
        print("=" * 60)
        print("TAHAP 1: ANALISIS LEKSIKAL")
        print("=" * 60)

        lexer = Lexer(self.code)

        try:
            for token in lexer.token_feed:
                print(token)
        except ValueError as e:
            print(f"Lexical Error: {e}")
            return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python bahasaku.py <file.bhs>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        program_code = f.read()

    program = bahasaKu(program_code)
    program.run()
