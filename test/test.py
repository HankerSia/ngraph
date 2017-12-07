#!/usr/bin/env python
# ----------------------------------------------------------------------------
# Copyright 2016 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------
import numpy as np

import pyngraph.util as util
from pyngraph import Float32, TensorViewType, Function
from pyngraph.op import Parameter, Add, Multiply
from pyngraph.runtime import Manager
from pyngraph.runtime import ParameterizedTensorViewFloat32

element_type = Float32.element_type()
print(type(element_type))
shape = [2,2]
A = Parameter(element_type, shape)
B = Parameter(element_type, shape)
C = Parameter(element_type, shape)
value_type = TensorViewType(element_type, shape)
parameter_list = [A, B, C]
function = Function(Multiply(Add(A, B), C), value_type, parameter_list, 'test')
manager = Manager.get('NGVM');
external = manager.compile(function)
backend = manager.allocate_backend()
cf = backend.make_call_frame(external)
a = backend.make_primary_tensor_view(element_type, shape)
b = backend.make_primary_tensor_view(element_type, shape)
c = backend.make_primary_tensor_view(element_type, shape)
result = backend.make_primary_tensor_view(element_type, shape)

a.write(Util.numpy_to_c(np.array([1,2,3,4], dtype=np.float32)), 0, 16)
b.write(Util.numpy_to_c(np.array([5,6,7,8], dtype=np.float32)), 0, 16)
c.write(Util.numpy_to_c(np.array([9,10,11,12], dtype=np.float32)), 0, 16)

a_arr = np.array([0, 0, 0, 0], dtype=np.float32)
b_arr = np.array([0, 0, 0, 0], dtype=np.float32)
c_arr = np.array([0, 0, 0, 0], dtype=np.float32)
a.read(Util.numpy_to_c(a_arr), 0, 16)
b.read(Util.numpy_to_c(b_arr), 0, 16)
c.read(Util.numpy_to_c(c_arr), 0, 16)
print('A = ', a_arr)
print('B = ', b_arr)
print('C = ', c_arr)

result_arr = np.array([0, 0, 0, 0], dtype=np.float32)
result.write(Util.numpy_to_c(result_arr), 0, 16)

cf.call([a, b, c], [result])

result.read(Util.numpy_to_c(result_arr), 0, 16)
print('Result = ', result_arr)
