// Copyright (C) 2018-2023 Intel Corporation
// SPDX-License-Identifier: Apache-2.0
//

/**
 * @file openvino/runtime/threading/cpu_streams_executor.hpp
 * @brief A header file for OpenVINO CPU-Streams-based Executor implementation.
 */

#pragma once

#include <memory>
#include <openvino/runtime/common.hpp>
#include <string>

#include "openvino/runtime/threading/istreams_executor.hpp"

namespace ov {
namespace threading {

/**
 * @class CPUStreamsExecutor
 * @ingroup ov_dev_api_threading
 * @brief CPU Streams executor implementation. The executor splits the CPU into groups of threads,
 *        that can be pinned to cores or NUMA nodes.
 *        It uses custom threads to pull tasks from single queue.
 */
class OPENVINO_RUNTIME_API CPUStreamsExecutor : public IStreamsExecutor {
public:
    /**
     * @brief Constructor
     * @param config Stream executor parameters
     */
    explicit CPUStreamsExecutor(const Config& config);

    /**
     * @brief A class destructor
     */
    ~CPUStreamsExecutor() override;

    void run(Task task) override;

    void execute(Task task) override;

    int get_stream_id() override;

    int get_numa_node_id() override;

private:
    struct Impl;
    std::unique_ptr<Impl> _impl;
};

}  // namespace threading
}  // namespace ov
