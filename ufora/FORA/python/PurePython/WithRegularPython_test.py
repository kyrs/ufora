#   Copyright 2015 Ufora Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import ufora.FORA.python.PurePython.InMemorySimulationExecutorFactory as \
    InMemorySimulationExecutorFactory
import pyfora.RemotePythonObject as RemotePythonObject
import pyfora.Exceptions as Exceptions
import pyfora.pure_modules.pure_pandas as PurePandas
import pyfora.helpers as helpers


import unittest
import traceback
import pandas

class EvaluateBodyAndReturnContext:
    def __enter__(self):
        pass

    def __exit__(self, excType, excValue, trace):
        pass

    def __pyfora_context_apply__(self, body):
        res =  __inline_fora(
            """fun(@unnamed_args:(body), ...) {
                       body()
                       }"""
                )(body)

        return res

class WithRegularPython_test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.executor = None

    @classmethod
    def tearDownClass(cls):
        if cls.executor is not None:
            cls.executor.close()

    @classmethod
    def create_executor(cls, allowCached=True):
        if not allowCached:
            return InMemorySimulationExecutorFactory.create_executor()
        if cls.executor is None:
            cls.executor = InMemorySimulationExecutorFactory.create_executor()
            cls.executor.stayOpenOnExit = True
        return cls.executor

    def test_internal_with_block_fails(self):
        with self.assertRaises(Exceptions.InvalidPyforaOperation):
            with self.create_executor() as fora:
                x = 5

                with fora.remotely:
                    z = 100

                    with z:
                        x = 100


    def test_basic_usage_of_with_block(self):
        with self.create_executor() as fora:
            x = 5

            with fora.remotely:
                z = 100

                with EvaluateBodyAndReturnContext():
                    z = z + x + 100


            result = z.toLocal().result()
            self.assertEqual(result, 205)

    def test_basic_out_of_process(self):
        with self.create_executor() as fora:
            x = 5

            with fora.remotely:
                z = 100

                with helpers.python:
                    z = z + x + 100

            result = z.toLocal().result()
            self.assertEqual(result, 205)

    def test_basic_out_of_process(self):
        with self.create_executor() as fora:
            x = 5

            with fora.remotely:
                z = 100

                with helpers.python:
                    z = z + x + 100

            result = z.toLocal().result()
            self.assertEqual(result, 205)

    def test_basic_out_of_process_variable_identities(self):
        with self.create_executor() as fora:
            x = {}

            with fora.remotely.downloadAll():
                with helpers.python:
                    #'x' is local to the with block - it won't be updated
                    x[10] = 20

                    #but the copy we send back will be because it gets 
                    #duplicated back into the surrounding context
                    y = x

            self.assertEqual(x, {})
            self.assertEqual(y, {10:20})
