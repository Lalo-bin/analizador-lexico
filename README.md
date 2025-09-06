# Analizador Léxico

Un analizador léxico (lexer) para un lenguaje de programación similar a C. Este proyecto analiza código fuente y genera tokens léxicos identificando palabras clave, operadores, identificadores, números, cadenas y comentarios.

## Características

- Reconoce palabras clave: `if`, `else`, `while`, `for`, `return`, `int`, `float`, `bool`, `string`, `true`, `false`, `void`, `break`, `continue`
- Identifica operadores: `++`, `--`, `&&`, `||`, `==`, `!=`, `>=`, `<=`, `+=`, `-=`, `*=`, `/=`, `%=`, `?`, `:`, `>`, `<`, `=`, `!`, `+`, `-`, `*`, `/`, `%`, `.`
- Reconoce puntuación: `(`, `)`, `{`, `}`, `[`, `]`, `,`, `;`
- Soporte para números enteros y flotantes (incluyendo notación científica)
- Procesamiento de cadenas de texto con secuencias de escape
- Comentarios de línea (`//`) y de bloque (`/* */`)
- Manejo de errores léxicos


## Estructura del Proyecto

```
analizador-lexico/
├── scan.py           # Programa principal
├── src/
│   └── lexer.py      # Implementación del analizador léxico
└── tests/            # Archivos de prueba
    ├── ok_minimo.tc
    ├── ok_borde.tc
    ├── error_string.tc
    ├── error_comentario.tc
    └── error_caracter_invalido.tc
```

## Ejecución
Desde el directorio del proyecto:

### Linux

1. **Ejecutar el analizador léxico**
   ```bash
   # Analizar un archivo específico
   python3 scan.py tests/ok_minimo.tc
   ```

2. **Ejecutar todas las pruebas**
   ```bash
   # Probar archivos válidos
   python3 scan.py tests/ok_minimo.tc
   python3 scan.py tests/ok_borde.tc
   
   # Probar archivos con errores (estos deben fallar)
   python3 scan.py tests/error_string.tc
   python3 scan.py tests/error_comentario.tc
   python3 scan.py tests/error_caracter_invalido.tc
   ```

### Windows
1. **Ejecutar el analizador léxico**
   ```cmd
   # Analizar un archivo específico
   python scan.py tests\ok_minimo.tc
   
   # O si tienes Python 3 específicamente
   py -3 scan.py tests\ok_minimo.tc
   ```

2. **Ejecutar todas las pruebas**
   ```cmd
   # Probar archivos válidos
   python scan.py tests\ok_minimo.tc
   python scan.py tests\ok_borde.tc
   
   # Probar archivos con errores (estos deben fallar)
   python scan.py tests\error_string.tc
   python scan.py tests\error_comentario.tc
   python scan.py tests\error_caracter_invalido.tc
   ```

## Formato de Salida

El programa muestra cada token encontrado en el formato:
```
TIPO_TOKEN  'lexema' @ línea:columna
```

### Ejemplo de salida:
```
KEYWORD    'int' @ 1:1
ID         'main' @ 1:5
PUNCT      '(' @ 1:9
PUNCT      ')' @ 1:10
PUNCT      '{' @ 1:12
KEYWORD    'float' @ 2:3
ID         'y' @ 2:9
OP         '=' @ 2:11
NUMBER     '3.14e-2' @ 2:13
PUNCT      ';' @ 2:20
```

## Manejo de Errores

El programa retorna diferentes códigos de salida:
- `0`: Análisis exitoso
- `1`: Error léxico encontrado
- `2`: Uso incorrecto (falta archivo de entrada)

## Archivos de Prueba

- `ok_minimo.tc`: Ejemplo básico con código válido
- `ok_borde.tc`: Casos límite válidos
- `error_string.tc`: Error en cadena de texto
- `error_comentario.tc`: Error en comentario
- `error_caracter_invalido.tc`: Carácter no reconocido

## Crear Tus Propios Archivos de Prueba

Puedes crear archivos con extensión `.tc` (o cualquier extensión) para probar el analizador:

```c
// ejemplo.tc
int x = 42;
float pi = 3.14159;
string mensaje = "Hola mundo\n";
if (x > 0) {
    x++;
}
```