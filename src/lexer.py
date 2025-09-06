import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

KEYWORDS = {
    "if","else","while","for","return","int","float","bool","string",
    "true","false","void","break","continue"
}

# Orden por "máxima coincidencia" primero
OPERATORS = [
    "++","--","&&","||","==","!=",">=","<=","+=","-=","*=","/=","%=",
    "?",
    ":",  # ternario separa, se emiten tokens ? y :
    ">", "<", "=", "!", "+", "-", "*", "/", "%", "."
]
PUNCT = {"(",")","{","}","[","]",",",";"}  # el "." va en operadores para permitir ".."

# Regex auxiliares compilados
RE_ID = re.compile(r'[_A-Za-z][_A-Za-z0-9]*')
RE_NUM = re.compile(r'(?:[0-9]+\.[0-9]*|\.[0-9]+|[0-9]+)(?:[eE][+\-]?[0-9]+)?')
RE_WS = re.compile(r'[ \t\r]+')  # no incluye \n para contar filas
RE_NEWLINE = re.compile(r'\n')

@dataclass
class Token:
    kind: str
    lexeme: str
    line: int
    col: int

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, src: str):
        self.src = src
        self.i = 0
        self.n = len(src)
        self.line = 1
        self.col = 1

    def peek(self, k=0) -> str:
        j = self.i + k
        return self.src[j] if j < self.n else ''

    def advance(self, k=1) -> None:
        for _ in range(k):
            if self.i >= self.n: return
            ch = self.src[self.i]
            self.i += 1
            if ch == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1

    def match_prefix(self, candidates: List[str]) -> Optional[str]:
        # Devuelve el operador más largo que coincida
        for op in sorted(candidates, key=lambda s: -len(s)):
            if self.src.startswith(op, self.i):
                return op
        return None

    def lex_string(self) -> Token:
        start_line, start_col = self.line, self.col
        assert self.peek() == '"'
        self.advance()  # consume "
        buf = []
        while True:
            if self.i >= self.n:
                raise LexerError(f"String sin cierre en {start_line}:{start_col}")
            ch = self.peek()
            if ch == '"':
                self.advance()
                break
            if ch == '\\':
                self.advance()
                esc = self.peek()
                if esc in ['"', '\\', 'n', 't', 'r', '0']:
                    mapping = {'n':'\n','t':'\t','r':'\r','0':'\0','"':'"','\\':'\\'}
                    buf.append(mapping[esc])
                    self.advance()
                else:
                    raise LexerError(f"Escape inválido '\\{esc}' en {self.line}:{self.col}")
            else:
                buf.append(ch)
                self.advance()
        return Token("STRING", ''.join(buf), start_line, start_col)

    def skip_comment_line(self):
        while self.i < self.n and self.peek() != '\n':
            self.advance()

    def skip_comment_block(self):
        self.advance(2)  # consume '/*'
        while self.i < self.n:
            if self.peek() == '*' and self.peek(1) == '/':
                self.advance(2)
                return
            self.advance()
        raise LexerError(f"Comentario bloque sin cierre antes de EOF")

    def tokens(self) -> List[Token]:
        out: List[Token] = []
        while self.i < self.n:
            ch = self.peek()

            # newline
            if ch == '\n':
                self.advance()
                continue

            # espacios (no \n)
            m = RE_WS.match(self.src, self.i)
            if m:
                consumed = m.end() - self.i
                self.advance(consumed)
                continue

            # comentarios
            if ch == '/' and self.peek(1) == '/':
                self.skip_comment_line()
                continue
            if ch == '/' and self.peek(1) == '*':
                self.skip_comment_block()
                continue

            # string
            if ch == '"':
                out.append(self.lex_string())
                continue

            # identificador o palabra clave
            m = RE_ID.match(self.src, self.i)
            if m:
                lex = m.group(0)
                kind = "KEYWORD" if lex in KEYWORDS else "IDENT"
                out.append(Token(kind, lex, self.line, self.col))
                self.advance(len(lex))
                continue

            # número (int/float)
            m = RE_NUM.match(self.src, self.i)
            if m:
                lex = m.group(0)
                kind = "FLOAT" if ('.' in lex or 'e' in lex or 'E' in lex) else "INT"
                out.append(Token(kind, lex, self.line, self.col))
                self.advance(len(lex))
                continue

            # operadores y puntuación
            op = self.match_prefix(OPERATORS)
            if op:
                kind = {
                    "++":"INC","--":"DEC","&&":"AND","||":"OR",
                    "==":"EQ","!=":"NEQ",">=":"GE","<=":"LE",
                    "+=":"PLUSEQ","-=":"MINUSEQ","*=":"MULTEQ","/=":"DIVEQ","%=":"MODEQ",
                    "+":"PLUS","-":"MINUS","*":"MUL","/":"DIV","%":"MOD",
                    ">":"GT","<":"LT","=":"ASSIGN","!":"NOT",
                    "?":"QMARK",":":"COLON",".":"DOT"
                }.get(op, "OP")
                out.append(Token(kind, op, self.line, self.col))
                self.advance(len(op))
                continue

            if ch in PUNCT:
                mapk = {
                    "(":"LPAREN",")":"RPAREN","{":"LBRACE","}":"RBRACE",
                    "[":"LBRACK","]":"RBRACK",",":"COMMA",";":"SEMI"
                }
                out.append(Token(mapk[ch], ch, self.line, self.col))
                self.advance()
                continue

            raise LexerError(f"Carácter inesperado '{ch}' en {self.line}:{self.col}")

        out.append(Token("EOF","", self.line, self.col))
        return out

if __name__ == "__main__":
    demo = r'''
      // demo
      int x = 10;
      float y = 3.14e-2;
      string s = "hola \"mundo\"\n";
      if (x >= y && y != 0) { x += 1; }
      /* bloque
         multi-linea */
      x++; y--; s = s + "!";
      a?.b:c; // si implementas ternario estricto, ? y : ya están
    '''
    toks = Lexer(demo).tokens()
    for t in toks:
        print(t)
