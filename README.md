# Stuff you gotta do thats not obviuos

 * Install Bazel (for Acme)
 *

https://github.com/hill-a/stable-baselines

Requirements:
 * Python 3.7.10
 * tensorflow 1.14.0 (Stable-Baselines supports Tensorflow versions from 1.8.0 to 1.14.0)
 * pyglet 1.5.11 (installing this will give a compatability error, but it really works...)


If you get this dumb error:
The headers or library files could not be found for zlib,
a required dependency when compiling Pillow from source.

See [this random solution](https://akrabat.com/installing-pillow-on-macos-10-15-calatalina/).

Tensorflow 1.14 only works with Python 3.7 or earlier, so download pyenv and create
a virtual environment with the command

```
pyenv virtualenv 3.7.10 goenv
pyenv local goenv # must run this from dir where you want to use env
```

https://stable-baselines.readthedocs.io/en/master/guide/custom_env.html
https://github.com/openai/gym/blob/master/docs/creating-environments.md

** policy class


https://ai.stackexchange.com/questions/11174/2-player-games-in-openai-retro


---------------------------------------
| approxkl           | 0.0            |
| clipfrac           | 0.0            |
| explained_variance | 5.96e-08       |
| fps                | 2294           |
| n_updates          | 151            |
| policy_entropy     | 6.5072115e-08  |
| policy_loss        | -4.4237822e-09 |
| serial_timesteps   | 19328          |
| time_elapsed       | 8.63           |
| total_timesteps    | 19328          |
| value_loss         | 1071.9443      |
---------------------------------------


https://github.com/openai/gym/blob/c8a659369d98706b3c98b84b80a34a832bbdc6c0/gym/core.py#L120


episode: game

verbose outputs gets printed every 128 timesteps, no matter what.

TODO: how to see what the reward is at each episode ?
TODO: how to design reward functions?

When applying RL to a custom problem, you should always normalize the input to the agent (e.g. using VecNormalize
for PPO2/A2C)

HYPERTUNE:

learning_rate=0.00025, total_timesteps=1000, nminibatches=4 -- mean -10
learning_rate=0.00025, total_timesteps=10000, nminibatches=4 -- mean -9 to -0
learning_rate=0.0025, total_timesteps=10000, nminibatches=4 -- mean 4.34
learning_rate=0.025, total_timesteps=10000, nminibatches=4 -- mean 0-3
learning_rate=0.0025, total_timesteps=10000, nminibatches=64 -- mean -9.6
learning_rate=0.0025, total_timesteps=10000, nminibatches=1 -- mean -1, 3.08
learning_rate=0.0025, total_timesteps=100000, nminibatches=4 -- 7.94

PLAYING AGAINST ITSELF (learning_rate=0.0025, total_timesteps=100000, nminibatches=4):

(Opponent is always O, opponent is trained against random in same run)
Training against random: 7.08, training against self: 6.18
Training against random: 8.46, training against self: 6.78
Training against random: 5.34, training against self: 2.7
