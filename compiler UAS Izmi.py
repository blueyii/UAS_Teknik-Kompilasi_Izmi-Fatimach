
import re

TOKEN_TYPES = [
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),
    ('ID', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('NUM', r'\b\d+\b'),
    ('OP', r'==|!=|>=|<=|>|<'),
    ('ASSIGN', r'='),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SEMICOLON', r';'),
    ('SKIP', r'[ \t\n]+'),
]

class Token:
    def __init__(self,t,v):
        self.type=t; self.value=v
    def __repr__(self):
        return f"({self.type}, '{self.value}')"

def tokenize(code):
    tokens=[]; pos=0
    while pos<len(code):
        m=None
        for t,p in TOKEN_TYPES:
            m=re.match(p,code[pos:])
            if m:
                txt=m.group(0)
                if t!="SKIP":
                    tokens.append(Token(t,txt))
                pos+=len(txt)
                break
        if not m:
            raise SyntaxError(f"Karakter ilegal: {code[pos]}")
    return tokens

class ASTNode: pass
class IfNode(ASTNode):
    def __init__(self,l,o,r,then_stmt,else_stmt):
        self.left=l; self.op=o; self.right=r
        self.then_stmt=then_stmt
        self.else_stmt=else_stmt
class AssignNode(ASTNode):
    def __init__(self,var,val):
        self.var=var; self.val=val

class Parser:
    def __init__(self,tokens):
        self.t=tokens; self.i=0
    def peek(self):
        return self.t[self.i] if self.i<len(self.t) else None
    def eat(self,tp):
        tok=self.peek()
        if tok and tok.type==tp:
            self.i+=1
            return tok
        raise SyntaxError(f"Expected {tp}, found {tok}")
    def parse(self):
        self.eat("IF"); self.eat("LPAREN")
        l=self.eat("ID").value
        op=self.eat("OP").value
        r=self.eat("NUM").value
        self.eat("RPAREN"); self.eat("LBRACE")
        tv=self.eat("ID").value
        self.eat("ASSIGN")
        tval=self.eat("NUM").value
        self.eat("SEMICOLON"); self.eat("RBRACE")
        self.eat("ELSE"); self.eat("LBRACE")
        ev=self.eat("ID").value
        self.eat("ASSIGN")
        evalv=self.eat("NUM").value
        self.eat("SEMICOLON"); self.eat("RBRACE")
        return IfNode(l,op,r,AssignNode(tv,tval),AssignNode(ev,evalv))

class SemanticAnalyzer:
    def __init__(self,symbols):
        self.symbols=symbols
    def analyze(self,node):
        if node.left not in self.symbols:
            raise NameError(f"Variabel '{node.left}' belum dideklarasikan")
        for a in [node.then_stmt,node.else_stmt]:
            if a.var not in self.symbols:
                raise NameError(f"Variabel '{a.var}' belum dideklarasikan")

class TACGenerator:
    def generate(self,node):
        return [
            f"t1 = {node.left} {node.op} {node.right}",
            "ifFalse t1 goto L1",
            f"{node.then_stmt.var} = {node.then_stmt.val}",
            "goto L2",
            "L1:",
            f"{node.else_stmt.var} = {node.else_stmt.val}",
            "L2:"
        ]

if __name__=="__main__":
    source="""
if (nilai > 75) {
    hasil = 1;
} else {
    hasil = 0;
}
"""
    table={"nilai":"int","hasil":"int"}
    print("=== KODE SUMBER ===")
    print(source.strip())
    print("-"*40)
    tok=tokenize(source)
    print("\n[1] HASIL ANALISIS LEKSIKAL (TOKENS):")
    print(tok)
    ast=Parser(tok).parse()
    print("\n[2] HASIL ANALISIS SINTAKSIS (AST BERHASIL DIBENTUK):")
    print(f"Root Node: IfNode")
    print(f"Condition : {ast.left} {ast.op} {ast.right}")
    print(f"Then      : {ast.then_stmt.var} = {ast.then_stmt.val}")
    print(f"Else      : {ast.else_stmt.var} = {ast.else_stmt.val}")
    SemanticAnalyzer(table).analyze(ast)
    print("\n[3] HASIL ANALISIS SEMANTIK:")
    print("Validasi sukses! Semua variabel terdaftar di Symbol Table.")
    print("\n[4] HASIL GENERASI KODE ANTARA (THREE-ADDRESS CODE):")
    for x in TACGenerator().generate(ast):
        print(x)
