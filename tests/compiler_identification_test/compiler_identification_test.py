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

import os
import unittest

from compiler_identification import CompilerIdentification

TEST_DATA_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'test_input')


def read_file(path: str) -> str:
    with open(path) as input_file:
        return input_file.read()


class TestCompilerIdentification(unittest.TestCase):
    def run_one_test(
            self,
            input_file_name: str) -> None:
        input_file_name += '.txt'
        file_name_components = input_file_name.split('-')
        expected_family = file_name_components[0]
        expected_version_str = file_name_components[1]
        compiler_identification = CompilerIdentification(
            read_file(os.path.join(TEST_DATA_DIR, input_file_name)))
        self.assertEqual(expected_family, compiler_identification.family)
        self.assertEqual(expected_version_str, compiler_identification.version_str)

    def test_clang10_apple(self) -> None:
        self.run_one_test('clang-10.0.1-macos')

    def test_clang10_centos7_yb_built(self) -> None:
        self.run_one_test('clang-10.0.1-centos7-yb-built')

    def test_clang11_centos7_yb_built(self) -> None:
        self.run_one_test('clang-11.0.0-centos7-yb-built')

    def test_clang11_ubuntu1804(self) -> None:
        self.run_one_test('clang-11.0.1-ubuntu1804')

    def test_gcc7_ubuntu(self) -> None:
        self.run_one_test('gcc-7.5.0-ubuntu')

    def test_gcc8_ubuntu(self) -> None:
        self.run_one_test('gcc-8.4.0-ubuntu')

    def test_gcc8_debian(self) -> None:
        self.run_one_test('gcc-8.3.0-debian')

    def test_gcc10_alpine(self) -> None:
        self.run_one_test('gcc-10.2.1-alpine')

    def test_clang10_alpine(self) -> None:
        self.run_one_test('clang-10.0.1-alpine')

    def test_clang12_macos_big_sur(self) -> None:
        self.run_one_test('clang-12.0.5-macos-11.2.3')


if __name__ == '__main__':
    unittest.main()
