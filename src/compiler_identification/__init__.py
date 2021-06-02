#!/usr/bin/env python3

# Copyright (c) Yugabyte, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations
# under the License.

import re
import subprocess
import os
from autorepr import autorepr, autotext  # type: ignore

from packaging.version import parse as parse_version
from packaging.version import Version

from typing import Optional, List, Pattern


NUMERIC_VERSION_RE_STR = r'([0-9]+(?:[.][0-9]+)*)'


def create_version_pattern(version_pattern_str: str) -> Pattern:
    return re.compile(version_pattern_str % NUMERIC_VERSION_RE_STR)


def create_version_patterns(version_patterns: List[str]) -> List[Pattern]:
    return [create_version_pattern(p) for p in version_patterns]


CLANG_VERSION_PATTERN = create_version_pattern(r'(?:LLVM|clang) version %s(?: |-|$|\b)')


GCC_VERSION_PATTERNS = create_version_patterns([
    r'gcc version %s ',
    r'gcc [(]GCC[)] %s ',
    # This is used on Debian, e.g. "gcc (Debian 8.3.0-6) 8.3.0". We skip what is in parentheses.
    r'gcc [(][^)]+[)] %s\b'
])


class CompilerIdentification:
    """
    Given a compiler, determines its version, its installation directory, and other information that
    might influence how we should build the code.
    """
    family: str
    version_str: str
    full_version_output_str: str
    parsed_version: Version
    compiler_path: Optional[str]

    __repr__ = __str__ = autorepr(
         ["family", "version_str", "full_version_output_str", "parsed_version", "compiler_path"])

    def _try_pattern(self, pattern: Pattern, family: str) -> bool:
        m = pattern.search(self.full_version_output_str)
        if m:
            self.version_str = m.group(1)
            self.family = family
            parsed_version = parse_version(self.version_str)
            assert isinstance(parsed_version, Version), (
                "Got an unexpected type of parsed version: %s" % parsed_version)
            self.parsed_version = parsed_version

            return True
        return False

    def __init__(self, full_version_output_str: str, compiler_path: Optional[str] = None):
        self.full_version_output_str = full_version_output_str.strip()
        self.compiler_path = compiler_path
        if self._try_pattern(CLANG_VERSION_PATTERN, 'clang'):
            return
        for gcc_version_pattern in GCC_VERSION_PATTERNS:
            if self._try_pattern(gcc_version_pattern, 'gcc'):
                return

        error_msg = "Could not identify the compiler. '-v' output: %s" % full_version_output_str
        if self.compiler_path is not None:
            error_msg += ". Compiler path: %s" % self.compiler_path
        raise ValueError(error_msg)

    def is_compatible_with(self, other: 'CompilerIdentification') -> bool:
        return self.family == other.family and self.version_str == other.version_str


def identify_compiler(compiler_path: str) -> CompilerIdentification:
    assert compiler_path

    if os.path.pathsep not in compiler_path:
        # When only given a compiler file name, try to resolve it against PATH, similar to the UNIX
        # "which" command.
        path_env_var = os.getenv("PATH")
        if path_env_var:
            for path_entry in path_env_var.split(os.path.pathsep):
                compiler_candidate_path = os.path.join(path_entry, compiler_path)
                if os.access(compiler_candidate_path, os.X_OK):
                    compiler_path = compiler_candidate_path
                    break

    if os.path.exists(compiler_path):
        # We only replace the path with an absolute path if we know it exists. Otherwise we might
        # get a confusing error later.
        compiler_path = os.path.abspath(compiler_path)

    proc = subprocess.Popen(
        [compiler_path, '-v'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout_bytes, stderr_bytes = proc.communicate()
    if proc.returncode != 0:
        raise IOError(
            f"Could not determine compiler version for '{compiler_path}': compiler invoked with "
            f"-v failed with exit code {proc.returncode}. Current directory: {os.getcwd()}.")

    output_str_candidates = []
    for output_bytes in [stdout_bytes, stderr_bytes]:
        output_str = output_bytes.decode('utf-8').strip()
        if not output_str:
            continue
        output_str_candidates.append(output_str)
        return CompilerIdentification(output_str, compiler_path)

    raise ValueError(
        f"Could not determine compiler version for '{compiler_path}'. "
        f"Output: {output_str_candidates}.")
