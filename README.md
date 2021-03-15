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
pyenv virtualenv 3.7.10 goenv


https://stable-baselines.readthedocs.io/en/master/guide/custom_env.html
https://github.com/openai/gym/blob/master/docs/creating-environments.md

** policy class
