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
