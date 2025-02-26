# -*- coding: utf-8 -*-
# Copyright (C) 2018-2023 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
import sys

import numpy as np

import openvino.runtime as ov
from openvino.runtime import Tensor
from openvino.helpers import pack_data, unpack_data

import pytest

from tests.test_utils.test_utils import generate_image


@pytest.mark.parametrize(("ov_type", "numpy_dtype"), [
    (ov.Type.f32, np.float32),
    (ov.Type.f64, np.float64),
    (ov.Type.f16, np.float16),
    (ov.Type.bf16, np.float16),
    (ov.Type.i8, np.int8),
    (ov.Type.u8, np.uint8),
    (ov.Type.i32, np.int32),
    (ov.Type.u32, np.uint32),
    (ov.Type.i16, np.int16),
    (ov.Type.u16, np.uint16),
    (ov.Type.i64, np.int64),
    (ov.Type.u64, np.uint64),
    (ov.Type.boolean, bool),
    (ov.Type.u1, np.uint8),
    (ov.Type.u4, np.uint8),
    (ov.Type.i4, np.int8),
])
def test_init_with_ngraph(ov_type, numpy_dtype):
    ov_tensors = []
    ov_tensors.append(Tensor(type=ov_type, shape=ov.Shape([1, 3, 32, 32])))
    ov_tensors.append(Tensor(type=ov_type, shape=[1, 3, 32, 32]))
    assert np.all([list(ov_tensor.shape) == [1, 3, 32, 32] for ov_tensor in ov_tensors])
    assert np.all(ov_tensor.element_type == ov_type for ov_tensor in ov_tensors)
    assert np.all(ov_tensor.data.dtype == numpy_dtype for ov_tensor in ov_tensors)
    assert np.all(ov_tensor.data.shape == (1, 3, 32, 32) for ov_tensor in ov_tensors)


def test_subprocess():
    args = [sys.executable, os.path.join(os.path.dirname(__file__), "subprocess_test_tensor.py")]

    status = subprocess.run(args, env=os.environ)
    assert not status.returncode


@pytest.mark.parametrize(("ov_type", "numpy_dtype"), [
    (ov.Type.f32, np.float32),
    (ov.Type.f64, np.float64),
    (ov.Type.f16, np.float16),
    (ov.Type.i8, np.int8),
    (ov.Type.u8, np.uint8),
    (ov.Type.i32, np.int32),
    (ov.Type.u32, np.uint32),
    (ov.Type.i16, np.int16),
    (ov.Type.u16, np.uint16),
    (ov.Type.i64, np.int64),
    (ov.Type.u64, np.uint64),
    (ov.Type.boolean, bool),
])
def test_init_with_numpy_dtype(ov_type, numpy_dtype):
    shape = (1, 3, 127, 127)
    ov_shape = ov.Shape(shape)
    ov_tensors = []
    ov_tensors.append(Tensor(type=numpy_dtype, shape=shape))
    ov_tensors.append(Tensor(type=np.dtype(numpy_dtype), shape=shape))
    ov_tensors.append(Tensor(type=np.dtype(numpy_dtype), shape=np.array(shape)))
    ov_tensors.append(Tensor(type=numpy_dtype, shape=ov_shape))
    ov_tensors.append(Tensor(type=np.dtype(numpy_dtype), shape=ov_shape))
    assert np.all(tuple(ov_tensor.shape) == shape for ov_tensor in ov_tensors)
    assert np.all(ov_tensor.element_type == ov_type for ov_tensor in ov_tensors)
    assert np.all(isinstance(ov_tensor.data, np.ndarray) for ov_tensor in ov_tensors)
    assert np.all(ov_tensor.data.dtype == numpy_dtype for ov_tensor in ov_tensors)
    assert np.all(ov_tensor.data.shape == shape for ov_tensor in ov_tensors)


@pytest.mark.parametrize(("ov_type", "numpy_dtype"), [
    (ov.Type.f32, np.float32),
    (ov.Type.f64, np.float64),
    (ov.Type.f16, np.float16),
    (ov.Type.i8, np.int8),
    (ov.Type.u8, np.uint8),
    (ov.Type.i32, np.int32),
    (ov.Type.u32, np.uint32),
    (ov.Type.i16, np.int16),
    (ov.Type.u16, np.uint16),
    (ov.Type.i64, np.int64),
    (ov.Type.u64, np.uint64),
    (ov.Type.boolean, bool),
])
def test_init_with_numpy_shared_memory(ov_type, numpy_dtype):
    arr = generate_image().astype(numpy_dtype)
    shape = arr.shape
    arr = np.ascontiguousarray(arr)
    ov_tensor = Tensor(array=arr, shared_memory=True)
    assert tuple(ov_tensor.shape) == shape
    assert ov_tensor.element_type == ov_type
    assert isinstance(ov_tensor.data, np.ndarray)
    assert ov_tensor.data.dtype == numpy_dtype
    assert ov_tensor.data.shape == shape
    assert np.shares_memory(arr, ov_tensor.data)
    assert np.array_equal(ov_tensor.data, arr)
    assert ov_tensor.size == arr.size
    assert ov_tensor.byte_size == arr.nbytes
    assert tuple(ov_tensor.strides) == arr.strides

    assert tuple(ov_tensor.get_shape()) == shape
    assert ov_tensor.get_element_type() == ov_type
    assert ov_tensor.get_size() == arr.size
    assert ov_tensor.get_byte_size() == arr.nbytes
    assert tuple(ov_tensor.get_strides()) == arr.strides


@pytest.mark.parametrize(("ov_type", "numpy_dtype"), [
    (ov.Type.f32, np.float32),
    (ov.Type.f64, np.float64),
    (ov.Type.f16, np.float16),
    (ov.Type.i8, np.int8),
    (ov.Type.u8, np.uint8),
    (ov.Type.i32, np.int32),
    (ov.Type.u32, np.uint32),
    (ov.Type.i16, np.int16),
    (ov.Type.u16, np.uint16),
    (ov.Type.i64, np.int64),
    (ov.Type.u64, np.uint64),
    (ov.Type.boolean, bool),
])
def test_init_with_numpy_copy_memory(ov_type, numpy_dtype):
    arr = generate_image().astype(numpy_dtype)
    shape = arr.shape
    ov_tensor = Tensor(array=arr, shared_memory=False)
    assert tuple(ov_tensor.shape) == shape
    assert ov_tensor.element_type == ov_type
    assert isinstance(ov_tensor.data, np.ndarray)
    assert ov_tensor.data.dtype == numpy_dtype
    assert ov_tensor.data.shape == shape
    assert not (np.shares_memory(arr, ov_tensor.data))
    assert np.array_equal(ov_tensor.data, arr)
    assert ov_tensor.size == arr.size
    assert ov_tensor.byte_size == arr.nbytes


def test_init_with_roi_tensor():
    array = np.random.normal(size=[1, 3, 48, 48])
    ov_tensor1 = Tensor(array)
    ov_tensor2 = Tensor(ov_tensor1, [0, 0, 24, 24], [1, 3, 48, 48])
    assert list(ov_tensor2.shape) == [1, 3, 24, 24]
    assert ov_tensor2.element_type == ov_tensor2.element_type
    assert np.shares_memory(ov_tensor1.data, ov_tensor2.data)
    assert np.array_equal(ov_tensor1.data[0:1, :, 24:, 24:], ov_tensor2.data)


@pytest.mark.parametrize(("ov_type", "numpy_dtype"), [
    (ov.Type.f32, np.float32),
    (ov.Type.f64, np.float64),
    (ov.Type.f16, np.float16),
    (ov.Type.bf16, np.float16),
    (ov.Type.i8, np.int8),
    (ov.Type.u8, np.uint8),
    (ov.Type.i32, np.int32),
    (ov.Type.u32, np.uint32),
    (ov.Type.i16, np.int16),
    (ov.Type.u16, np.uint16),
    (ov.Type.i64, np.int64),
    (ov.Type.u64, np.uint64),
    (ov.Type.boolean, bool),
])
def test_write_to_buffer(ov_type, numpy_dtype):
    ov_tensor = Tensor(ov_type, ov.Shape([1, 3, 32, 32]))
    ones_arr = np.ones([1, 3, 32, 32], numpy_dtype)
    ov_tensor.data[:] = ones_arr
    assert np.array_equal(ov_tensor.data, ones_arr)


@pytest.mark.parametrize(("ov_type", "numpy_dtype"), [
    (ov.Type.f32, np.float32),
    (ov.Type.f64, np.float64),
    (ov.Type.f16, np.float16),
    (ov.Type.bf16, np.float16),
    (ov.Type.i8, np.int8),
    (ov.Type.u8, np.uint8),
    (ov.Type.i32, np.int32),
    (ov.Type.u32, np.uint32),
    (ov.Type.i16, np.int16),
    (ov.Type.u16, np.uint16),
    (ov.Type.i64, np.int64),
    (ov.Type.u64, np.uint64),
    (ov.Type.boolean, bool),
])
def test_set_shape(ov_type, numpy_dtype):
    shape = ov.Shape([1, 3, 32, 32])
    ref_shape = ov.Shape([1, 3, 48, 48])
    ref_shape_np = [1, 3, 28, 28]
    ov_tensor = Tensor(ov_type, shape)

    ov_tensor.set_shape(ref_shape)
    assert list(ov_tensor.shape) == list(ref_shape)
    ov_tensor.shape = ref_shape
    assert list(ov_tensor.shape) == list(ref_shape)

    ones_arr = np.ones(list(ov_tensor.shape), numpy_dtype)
    ov_tensor.data[:] = ones_arr
    assert np.array_equal(ov_tensor.data, ones_arr)

    ov_tensor.set_shape(ref_shape_np)
    assert list(ov_tensor.shape) == ref_shape_np
    ov_tensor.shape = ref_shape_np
    assert list(ov_tensor.shape) == ref_shape_np

    zeros = np.zeros(ref_shape_np, numpy_dtype)
    ov_tensor.data[:] = zeros
    assert np.array_equal(ov_tensor.data, zeros)


@pytest.mark.parametrize("ref_shape", [
    [1, 3, 24, 24],
    [1, 3, 32, 32],
])
def test_can_set_smaller_or_same_shape_on_preallocated_memory(ref_shape):
    ones_arr = np.ones(shape=(1, 3, 32, 32), dtype=np.float32)
    ones_arr = np.ascontiguousarray(ones_arr)
    ov_tensor = Tensor(ones_arr, shared_memory=True)
    assert np.shares_memory(ones_arr, ov_tensor.data)
    ov_tensor.shape = ref_shape
    assert list(ov_tensor.shape) == ref_shape


def test_cannot_set_bigger_shape_on_preallocated_memory():
    ones_arr = np.ones(shape=(1, 3, 32, 32), dtype=np.float32)
    ones_arr = np.ascontiguousarray(ones_arr)
    ov_tensor = Tensor(ones_arr, shared_memory=True)
    ref_shape = [1, 3, 48, 48]
    assert np.shares_memory(ones_arr, ov_tensor.data)
    with pytest.raises(RuntimeError) as e:
        ov_tensor.shape = ref_shape
    assert "Cannot call setShape for Blobs created on top of preallocated memory" in str(e.value)


@pytest.mark.skip(reason="no support yet")
def test_can_reset_shape_after_decreasing_on_preallocated_memory():
    ones_arr = np.ones(shape=(1, 3, 32, 32), dtype=np.float32)
    ones_arr = np.ascontiguousarray(ones_arr)
    ov_tensor = Tensor(ones_arr, shared_memory=True)
    ref_shape_1 = [1, 3, 24, 24]
    ref_shape_2 = [1, 3, 32, 32]
    assert np.shares_memory(ones_arr, ov_tensor.data)
    ov_tensor.shape = ref_shape_1
    assert list(ov_tensor.shape) == ref_shape_1
    ov_tensor.shape = ref_shape_2
    assert list(ov_tensor.shape) == ref_shape_2


def test_cannot_set_shape_incorrect_dims():
    ov_tensor = Tensor(np.float32, [1, 3, 48, 48])
    with pytest.raises(RuntimeError) as e:
        ov_tensor.shape = [3, 28, 28]
    assert "Dims and format are inconsistent" in str(e.value)


@pytest.mark.parametrize("ov_type", [
    (ov.Type.u1),
    (ov.Type.u4),
    (ov.Type.i4),
])
def test_cannot_create_roi_from_packed_tensor(ov_type):
    ov_tensor = Tensor(ov_type, [1, 3, 48, 48])
    with pytest.raises(RuntimeError) as e:
        Tensor(ov_tensor, [0, 0, 24, 24], [1, 3, 48, 48])
    assert "ROI Tensor for types with bitwidths less then 8 bit is not implemented" in str(e.value)


@pytest.mark.parametrize("ov_type", [
    (ov.Type.u1),
    (ov.Type.u4),
    (ov.Type.i4),
])
def test_cannot_get_strides_for_packed_tensor(ov_type):
    ov_tensor = Tensor(ov_type, [1, 3, 48, 48])
    with pytest.raises(RuntimeError) as e:
        ov_tensor.get_strides()
    assert "Could not get strides for types with bitwidths less then 8 bit." in str(e.value)


@pytest.mark.parametrize("dtype", [
    (np.uint8),
    (np.int8),
    (np.uint16),
    (np.uint32),
    (np.uint64),
])
@pytest.mark.parametrize("ov_type", [
    (ov.Type.u1),
    (ov.Type.u4),
    (ov.Type.i4),
])
def test_init_with_packed_buffer(dtype, ov_type):
    shape = [1, 3, 32, 32]
    fit = np.dtype(dtype).itemsize * 8 / ov_type.bitwidth
    assert np.prod(shape) % fit == 0
    size = int(np.prod(shape) // fit)
    buffer = np.random.normal(size=size).astype(dtype)
    ov_tensor = Tensor(buffer, shape, ov_type)
    assert ov_tensor.data.nbytes == ov_tensor.byte_size
    assert np.array_equal(ov_tensor.data.view(dtype), buffer)


@pytest.mark.parametrize("shape", [
    ([1, 3, 28, 28]),
    ([1, 3, 27, 27]),
])
@pytest.mark.parametrize(("low", "high", "ov_type", "dtype"), [
    (0, 2, ov.Type.u1, np.uint8),
    (0, 16, ov.Type.u4, np.uint8),
    (-8, 7, ov.Type.i4, np.int8),
])
def test_packing(shape, low, high, ov_type, dtype):
    ov_tensor = Tensor(ov_type, shape)
    data = np.random.uniform(low, high, shape).astype(dtype)
    packed_data = pack_data(data, ov_tensor.element_type)
    ov_tensor.data[:] = packed_data
    unpacked = unpack_data(ov_tensor.data, ov_tensor.element_type, ov_tensor.shape)
    assert np.array_equal(unpacked, data)


@pytest.mark.parametrize("dtype", [
    (np.uint8),
    (np.int8),
    (np.int16),
    (np.uint16),
    (np.int32),
    (np.uint32),
    (np.int64),
    (np.uint64),
    (np.float16),
    (np.float32),
    (np.float64),
])
@pytest.mark.parametrize("element_type", [
    (ov.Type.u8),
    (ov.Type.i8),
    (ov.Type.i16),
    (ov.Type.u16),
    (ov.Type.i32),
    (ov.Type.u32),
    (ov.Type.i64),
    (ov.Type.u64),
])
def test_viewed_tensor(dtype, element_type):
    buffer = np.random.normal(size=(2, 16)).astype(dtype)
    fit = (dtype().nbytes * 8) / element_type.bitwidth
    tensor = Tensor(buffer, (buffer.shape[0], int(buffer.shape[1] * fit)), element_type)
    assert np.array_equal(tensor.data, buffer.view(ov.utils.types.get_dtype(element_type)))


def test_viewed_tensor_default_type():
    buffer = np.random.normal(size=(2, 16))
    new_shape = (4, 8)
    tensor = Tensor(buffer, new_shape)
    assert np.array_equal(tensor.data, buffer.reshape(new_shape))
