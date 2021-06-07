# compiler-identification

https://pypi.org/project/compiler-identification/

A useful tool in identifying the version of C/C++ compilers, mainly various versions of GCC and
Clang present in various Linux districtions and versions of macOS.

Usage (an ipython session shown):

```
In [1]: from compiler_identification import identify_compiler

In [2]: identification = identify_compiler('clang')

In [3]: identification
Out[3]: <compiler_identification.CompilerIdentification family='clang' version_str='12.0.5' full_version_output_str='Apple clang version 12.0.5 (clang-1205.0.22.9)\nTarget: x86_64-apple-darwin20.3.0\nThread model: posix\nInstalledDir: /Library/Developer/CommandLineTools/usr/bin' parsed_version=<Version('12.0.5')> compiler_path='/usr/bin/clang' at 0x7f904a95e970>

In [4]: identification.parsed_version
Out[4]: <Version('12.0.5')>
```

The `parsed_version`, which is a `Version` instance from the [`packaging`](https://pypi.org/project/packaging/) module, allows to do proper version comparisons.
