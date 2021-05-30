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

.PHONY: venv check
.DEFAULT: check

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
VENV_PYTHON=$(VENV_NAME)/bin/python3

venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: setup.py
	[[ -d "$(VENV_NAME)" ]] || python3 -m venv "$(VENV_NAME)"
	$(VENV_PYTHON) -m pip install --upgrade pip wheel
	$(VENV_PYTHON) -m pip install --editable '.[dev]'
	touch "$(VENV_NAME)/bin/activate"

check: venv
	$(VENV_PYTHON) -m codecheck --python-interpreter "$(VENV_PYTHON)"
	# Run tests again, although codecheck should have run them.
	$(VENV_PYTHON) -m unittest discover -s tests -p '*_test.py'

clean:
	git clean -dxf

