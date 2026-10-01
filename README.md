# sympy-ape

SymPy as a portable CLI, and from Node.js or Java, without installing Python.

`sympy-ape` packages SymPy 1.14.0 in a Cosmopolitan `sympy.com`, then exposes
the same commands through language-native bindings generated with
[APEBind](https://github.com/nuwainfo/apebind) 0.4.2. No system Python or
SymPy installation is required to call the bindings.

## Use `sympy.com`

```sh
./sympy.com integrate 'sin(x)'
# {"result": "-cos(x)", "latex": "- \\cos{\\left(x \\right)}"}
./sympy.com integrate --text 'sin(x)'
# -cos(x)
./sympy.com diff --order 2 'x**3'
./sympy.com solve 'x**2-1'
```

Each command prints one JSON object, `{"result", "latex"}`. `--text` prints
only the result string. The commands are `version`, `eval`, `simplify`,
`expand`, `factor`, `apart`, `diff`, `integrate`, `solve`, `limit`, `series`,
`subs`, and `numeric`.

## Bindings

Node.js:

```js
import { integrate, diff } from 'sympy-ape';

console.log(await integrate({ expr: 'sin(x)' }));
console.log(await diff({ expr: '-x**2' }));
```

Java:

```java
import apebind.generated.sympy_ape.SympyAPEBinding;

var value = SympyAPEBinding.integrate(
    SympyAPEBinding.IntegrateParameters.builder()
        .expr("sin(x)")
        .build());
```

The reviewed contract is [sympy.apebind.yaml](sympy.apebind.yaml). `version`
returns the version string. The other operations return the whole JSON object.
`--text` stays on the CLI and is omitted from the schema. The `eval` command
is exposed as `evaluate`, and `--var` is exposed as `symbols`.

## Build `sympy.com`

`sympy.com` is produced by the sibling
[pythoncosmofy](../pythoncosmofy) SymPy example. That folder downloads SymPy
and mpmath, applies the ctypes fallback required by `python.com`, and bundles
the CLI. Copy the resulting executable here, then regenerate the bindings
with the APEBind 0.4.2 binary in [apebind/dist](../apebind/dist/apebind.com):

```sh
../apebind/dist/apebind.com validate sympy.apebind.yaml
../apebind/dist/apebind.com generate sympy.apebind.yaml \
  --ape sympy.com --lang node -o bindings/node
../apebind/dist/apebind.com generate sympy.apebind.yaml \
  --ape sympy.com --lang java -o bindings/java
```

Regenerating replaces the generated sources under `bindings/`. The Node.js
tests and the Java smoke class live outside those generated trees.

## Test

```sh
./scripts/test.sh
```

That runs the `sympy.com` checks, the Node.js binding, and the Java binding.
Java requires a JDK 17 `javac`.
