# Copyright 2017 reinforce.io. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
from tensorforce import util
from tensorforce.core.preprocessing import Preprocessor


class Normalize(Preprocessor):
    """
    Normalize state. Subtract minimal value and divide by range.
    """

    def __init__(self, scope='normalize', summary_labels=()):
        super(Normalize).__init__(scope, summary_labels)

    def tf_process(self, tensor):
        # Min/max across every axis except batch dimension.
        min = tf.reduce_min(input_tensor=tensor, axis=np.arange(1, util.rank(tensor)))
        max = tf.reduce_max(input_tensor=tensor, axis=np.arange(1, util.rank(tensor)))

        return (tensor - min) / (max - min + util.epsilon)
