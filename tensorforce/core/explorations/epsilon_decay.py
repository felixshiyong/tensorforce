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

from tensorforce.core.explorations import Exploration
import tensorflow as tf

class EpsilonDecay(Exploration):
    """
    Exponentially decaying epsilon parameter based on ratio of
    difference between current and final epsilon to total timesteps.
    """

    def __init__(
        self,
        initial_epsilon=1.0,
        final_epsilon=0.1,
        timesteps=10000,
        start_timestep=0,
        half_lives=10,
        scope='epsilon_anneal',
        summary_labels=()
    ):
        self.initial_epsilon = initial_epsilon
        self.final_epsilon = final_epsilon
        self.timesteps = timesteps
        self.start_timestep = start_timestep
        self.half_life = timesteps / half_lives

        super(EpsilonDecay).__init__(scope, summary_labels)

    def tf_explore(self, episode=0, timestep=0, num_actions=1):
        def true_fn():
            # Know if first is not true second must be true from outer cond check.
            return tf.cond(
                pred=timestep < self.start_timestep,
                true_fn=(lambda: self.initial_epsilon),
                false_fn=(lambda: self.final_epsilon)
            )

        def false_fn():
            half_life_ratio = (tf.cast(x=timestep, dtype=tf.float32)
                               - tf.cast(x=self.start_timestep, dtype=tf.float32)) / tf.constant(value=self.half_life)
            epsilon = self.final_epsilon + (2 ** (-half_life_ratio)) * (self.initial_epsilon - self.final_epsilon)
            return tf.cast(x=epsilon, dtype=tf.float32)

        # Ternary evaluation. Check first two in first predicate, then both again in inner cond in true function.
        return tf.cond(
            pred=tf.logical_or(timestep < self.start_timestep, timestep > self.start_timestep + self.timesteps),
            true_fn=true_fn,
            false_fn=false_fn
        )


