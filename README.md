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

## Proximal Policy Optimization
Training data is itself dependent on the current policy.

PPO: policy gradient method

advantage function: discounted rewards - value function
discounted rewards: rewards up to this point (adjusted slightly so that sooner is better)
value function: estimate of discounted rewards from this point onward, predicted by NN



DQN:


WITH JUST PLAYING PREVIOUS:

round 0........
random opponent: mean reward: -1.02, std reward 9.9478439875181
round 1........
random opponent: mean reward: 3.72, std reward 9.282327294380435
last opponent: mean reward: 0.68, std reward 9.976853211308665
round 2........
random opponent: mean reward: 1.02, std reward 9.9478439875181
last opponent: mean reward: -5.4, std reward 8.416650165000325
round 3........
random opponent: mean reward: 6.04, std reward 7.969843160313758
last opponent: mean reward: 0.13, std reward 9.994153290799575
round 4........
random opponent: mean reward: 9.78, std reward 2.0860488968382316
last opponent: mean reward: 8.1, std reward 5.8642987645583
round 5........
random opponent: mean reward: 8.02, std reward 5.939663290120072
last opponent: mean reward: 6.53, std reward 7.447086678695233
round 6........
random opponent: mean reward: 7.78, std reward 6.28264275603826
last opponent: mean reward: 8.54, std reward 5.202730052578166
round 7........
random opponent: mean reward: 6.94, std reward 7.199749995659572
last opponent: mean reward: 8.64, std reward 5.034918072819061
round 8........
random opponent: mean reward: 7.74, std reward 6.331855968039704
last opponent: mean reward: 9.58, std reward 2.8676819907374664
round 9........
random opponent: mean reward: 7.72, std reward 6.356225294937238
last opponent: mean reward: 9.74, std reward 2.2654800815721163

--------

round 0........
random opponent: mean reward: 0.64, std reward 9.979498985420058
round 1........
random opponent: mean reward: 9.4, std reward 3.3823069050575527
last opponent: mean reward: 8.09, std reward 5.766446045876091
round 2........
random opponent: mean reward: 8.72, std reward 4.895058733049074
last opponent: mean reward: 7.92, std reward 6.072363625475669
round 3........
random opponent: mean reward: 9.37, std reward 3.4500869554259066
last opponent: mean reward: 4.67, std reward 8.723021265593706
round 4........
random opponent: mean reward: 7.8, std reward 6.257795138864806
last opponent: mean reward: 0.25, std reward 9.9818585443794
round 5........
random opponent: mean reward: 9.4, std reward 3.411744421846396
last opponent: mean reward: 6.37, std reward 7.504871751069436
round 6........
random opponent: mean reward: 9.01, std reward 4.326649974287266
last opponent: mean reward: 7.59, std reward 6.347590093886025
round 7........
random opponent: mean reward: 9.19, std reward 3.9043437348676147
last opponent: mean reward: 7.9, std reward 5.881326381013046
round 8........
random opponent: mean reward: 8.3, std reward 5.577633906953737
last opponent: mean reward: 9.27, std reward 3.5450105782634838
round 9........
random opponent: mean reward: 4.74, std reward 8.80524843488246
last opponent: mean reward: 7.87, std reward 5.9298482274000905


WITH PLAYING ALL PREVIOUS:
round 0........
random opponent: mean reward: -3.32, std reward 9.432793859721519
round 1........
random opponent: mean reward: 4.96, std reward 8.68322520726026
last opponent: mean reward: 3.78, std reward 9.258055951440346
round 2........
random opponent: mean reward: 5.62, std reward 8.259273575805564
last opponent: mean reward: -0.92, std reward 9.9475424100629
round 3........
random opponent: mean reward: 6.14, std reward 7.893060243023615
last opponent: mean reward: -2.94, std reward 9.558054195284729
round 4........
random opponent: mean reward: 7.52, std reward 6.591631057636644
last opponent: mean reward: 2.58, std reward 9.661449166662317
round 5........
random opponent: mean reward: 8.93, std reward 4.48944317259947
last opponent: mean reward: 3.67, std reward 9.296832794021842
round 6........
random opponent: mean reward: 8.87, std reward 4.6068535900330065
last opponent: mean reward: 0.07, std reward 9.954652178755419
round 7........
random opponent: mean reward: 9.54, std reward 2.9980660433019146
last opponent: mean reward: 7.19, std reward 6.870509442537723
round 8........
random opponent: mean reward: 9.37, std reward 3.4500869554259066
last opponent: mean reward: 7.11, std reward 6.47671984881236
round 9........
random opponent: mean reward: 8.63, std reward 5.042132485367674
last opponent: mean reward: 9.23, std reward 3.7292224390615263

-------

round 0........
random opponent: mean reward: -2.2, std reward 9.754998718605757
round 1........
random opponent: mean reward: 5.72, std reward 8.20253619315392
last opponent: mean reward: 3.3, std reward 9.439809320108115
round 2........
random opponent: mean reward: 8.98, std reward 4.399954545219757
last opponent: mean reward: 5.04, std reward 8.637036528810098
round 3........
random opponent: mean reward: 8.88, std reward 4.598434516223972
last opponent: mean reward: 7.78, std reward 6.282642756038259
round 4........
random opponent: mean reward: 8.9, std reward 4.559605246071198
last opponent: mean reward: 7.9, std reward 6.131068422387732
round 5........
random opponent: mean reward: 9.58, std reward 2.8676819907374664
last opponent: mean reward: 7.5, std reward 6.614378277661476
round 6........
random opponent: mean reward: 8.26, std reward 5.636701162914351
last opponent: mean reward: 8.7, std reward 4.930517214248421
round 7........
random opponent: mean reward: 9.48, std reward 3.182703253525217
last opponent: mean reward: 9.36, std reward 3.52
round 8........
random opponent: mean reward: 7.5, std reward 6.614378277661476
last opponent: mean reward: 9.5, std reward 3.122498999199199
round 9........
random opponent: mean reward: 8.86, std reward 4.636852380656516
last opponent: mean reward: 9.9, std reward 1.4106735979665883


WITH BIAS TOWARDS LATEST 2 MODELS:

round 0........
random opponent: mean reward: 3.78, std reward 9.247248239341259
round 1........
random opponent: mean reward: 1.0, std reward 9.9498743710662
last opponent: mean reward: -2.99, std reward 9.537289971475126
round 2........
random opponent: mean reward: 7.66, std reward 6.397218145412895
last opponent: mean reward: 3.19, std reward 9.38743308897592
round 3........
random opponent: mean reward: 9.67, std reward 2.5280624992274228
last opponent: mean reward: 4.15, std reward 9.03756051155399
round 4........
random opponent: mean reward: 8.78, std reward 4.786606313454242
last opponent: mean reward: 6.15, std reward 7.840758891842038
round 5........
random opponent: mean reward: 8.9, std reward 4.559605246071198
last opponent: mean reward: 7.87, std reward 6.1125362984607285
round 6........
random opponent: mean reward: 9.1, std reward 4.146082488325576
last opponent: mean reward: 8.98, std reward 4.399954545219756
round 7........
random opponent: mean reward: 8.84, std reward 4.674868982121318
last opponent: mean reward: 9.04, std reward 4.275324549083964
round 8........
random opponent: mean reward: 6.72, std reward 7.405511461067358
last opponent: mean reward: 9.62, std reward 2.730494460715861
round 9........
random opponent: mean reward: 8.1, std reward 5.864298764558301
last opponent: mean reward: 9.22, std reward 3.8718987590070073

---

round 0........
random opponent: mean reward: 6.47, std reward 7.618339714137195
round 1........
random opponent: mean reward: 2.1, std reward 9.77701385904715
last opponent: mean reward: -1.56, std reward 9.877570551507088
round 2........
random opponent: mean reward: 9.08, std reward 4.1657652358240265
last opponent: mean reward: 4.93, std reward 8.694544266377621
round 3........
random opponent: mean reward: 9.63, std reward 2.6763968315629136
last opponent: mean reward: 7.47, std reward 6.625639591767725
round 4........
random opponent: mean reward: 7.92, std reward 6.105210889068453
last opponent: mean reward: 5.69, std reward 8.217292741529901
round 5........
random opponent: mean reward: 9.38, std reward 3.466352549871406
last opponent: mean reward: 5.88, std reward 8.088609274776474
round 6........
random opponent: mean reward: 9.49, std reward 3.136861488813302
last opponent: mean reward: 5.59, std reward 8.188522455241849
round 7........
random opponent: mean reward: 6.11, std reward 7.909987357764865
last opponent: mean reward: 8.11, std reward 5.6504778558985596
round 8........
random opponent: mean reward: 5.4, std reward 8.416650165000325
last opponent: mean reward: 9.56, std reward 2.7214701909078483
round 9........
random opponent: mean reward: 6.76, std reward 7.355433365886744
last opponent: mean reward: 9.37, std reward 3.3620083283656514



## TODO:

Motivation: why was random doing so well? Because opponent sucked (made tons of
  illegal moves) because it was forced by play O but has just learned X.   

 * make players learn both sides
 * pass which color's turn it is to the player (necessary because otherwise NN has to learn who goes first)



SAMPLE OF PROBLEM:

[after 50 rounds training, agent is O]


random opponent: mean reward: -2.6, std reward 9.656086163658648
last opponent: mean reward: 9.96, std reward 0.893532316147547
GAME 0:
on step 0:
O . X
. . .
. . .
---
on step 1:
O . X
O X .
. . .
---
on step 2:
O . X
O X .
O . .
---
GAME 1:
on step 0:
O . X
. . .
. . .
---
on step 1:
O . X
O X .
. . .
---
on step 2:
O . X
O X .
O . .
---
GAME 2:
on step 0:
O . X
. . .
. . .
---
on step 1:
O . X
O X .
. . .
---
on step 2:
O . X
O X .
O . .
---
GAME 3:
on step 0:
O . X
. . .
. . .
---
on step 1:
O . X
O X .
. . .
---
on step 2:
O . X
O X .
O . .
---
GAME 4:
on step 0:
O . X
. . .
. . .
---
on step 1:
O . X
O X .
. . .
---
on step 2:
O . X
O X .
O . .
