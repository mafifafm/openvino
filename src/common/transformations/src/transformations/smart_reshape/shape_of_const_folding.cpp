// Copyright (C) 2018-2023 Intel Corporation
// SPDX-License-Identifier: Apache-2.0
//

#include "transformations/smart_reshape/shape_of_const_folding.hpp"

#include <openvino/core/rt_info.hpp>

#include "itt.hpp"
#include "openvino/core/validation_util.hpp"
#include "openvino/op/shape_of.hpp"
#include "openvino/opsets/opset10.hpp"
#include "openvino/pass/pattern/op/wrap_type.hpp"

ov::pass::ShapeOfConstFolding::ShapeOfConstFolding() {
    MATCHER_SCOPE(ShapeOfConstFolding);
    auto constant_label = pattern::wrap_type<opset10::Constant>();
    auto shape_of_label = pattern::wrap_type<op::v0::ShapeOf, opset10::ShapeOf>({constant_label});

    matcher_pass_callback callback = [=](pattern::Matcher& m) -> bool {
        auto node = m.get_match_root();
        if (auto constant = get_constant_from_source(node)) {
            constant->set_friendly_name(node->get_friendly_name());
            copy_runtime_info(node, constant);
            replace_node(node, constant);
            return true;
        }

        return false;
    };

    auto m = std::make_shared<pattern::Matcher>(shape_of_label, matcher_name);
    register_matcher(m, callback);
}
