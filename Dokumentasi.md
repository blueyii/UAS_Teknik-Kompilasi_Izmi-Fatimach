# Dokumentasi Proyek Akhir

## Representasi Tahapan Kompilasi -- Konstruksi `if-else`

### Nama Konstruksi

Percabangan **if-else**

------------------------------------------------------------------------

# 1. Tujuan

Program ini dibuat untuk mensimulasikan tahapan dasar proses kompilasi,
yaitu:

1.  Analisis Leksikal (Lexical Analysis)
2.  Analisis Sintaksis (Syntax Analysis)
3.  Analisis Semantik (Semantic Analysis)
4.  Generasi Kode Antara (Three-Address Code / TAC)

Program ditulis menggunakan bahasa **Python**.

------------------------------------------------------------------------

# 2. Grammar (BNF)

``` bnf
<if_stmt> ::= "if" "(" <condition> ")" "{"
              <assignment>
             "}" "else" "{"
              <assignment>
             "}"

<condition> ::= <identifier> <operator> <number>

<assignment> ::= <identifier> "=" <number> ";"

<identifier> ::= letter(letter|digit)*

<number> ::= digit+

<operator> ::= > | < | >= | <= | == | !=
```

------------------------------------------------------------------------

# 3. Analisis Leksikal

Tahap ini bertugas membaca source code kemudian mengubahnya menjadi
token.

Contoh input:

``` c
if (nilai > 75) {
    hasil = 1;
} else {
    hasil = 0;
}
```

Contoh token yang dihasilkan:

-   IF
-   LPAREN
-   ID
-   OP
-   NUM
-   RPAREN
-   LBRACE
-   ASSIGN
-   SEMICOLON
-   ELSE

------------------------------------------------------------------------

# 4. Analisis Sintaksis

Parser memeriksa apakah urutan token sesuai grammar.

Apabila struktur program tidak sesuai grammar maka program akan
menghasilkan **Syntax Error**.

Jika valid maka parser membentuk **Abstract Syntax Tree (AST)**.

Root AST:

    IfNode

Node turunannya:

-   Condition
-   Then Statement
-   Else Statement

------------------------------------------------------------------------

# 5. Analisis Semantik

Tahap semantik memastikan bahwa variabel yang digunakan telah terdaftar
pada **Symbol Table**.

Contoh:

  Variabel   Tipe
  ---------- ------
  nilai      int
  hasil      int

Apabila terdapat variabel yang belum dideklarasikan maka compiler akan
menampilkan pesan kesalahan semantik.

------------------------------------------------------------------------

# 6. Three-Address Code (TAC)

AST diterjemahkan menjadi kode antara (Intermediate Code).

Contoh hasil TAC:

``` text
t1 = nilai > 75
ifFalse t1 goto L1
hasil = 1
goto L2
L1:
hasil = 0
L2:
```

------------------------------------------------------------------------

# 7. Cara Menjalankan Program

Buka terminal pada folder project kemudian jalankan:

``` bash
python compiler_if_else.py
```

------------------------------------------------------------------------

# 8. Kesimpulan

Program berhasil mensimulasikan proses kompilasi sederhana pada
konstruksi **if-else**.

Tahapan yang berhasil direpresentasikan meliputi:

-   Analisis Leksikal
-   Analisis Sintaksis
-   Pembentukan AST
-   Analisis Semantik
-   Generasi Three-Address Code (TAC)

Walaupun masih sederhana, implementasi ini telah menggambarkan alur
kerja dasar sebuah compiler dalam memproses source code hingga
menghasilkan representasi kode antara.
