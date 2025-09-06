import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from lexer import Lexer, LexerError

def scan_text(text: str):
    toks = Lexer(text).tokens()
    for t in toks:
        print(f"{t.kind:<10} {t.lexeme!r} @ {t.line}:{t.col}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scan.py <archivo>")
        sys.exit(2)
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    try:
        scan_text(src)
        sys.exit(0)
    except LexerError as e:
        print("ERROR:", e)
        sys.exit(1)
