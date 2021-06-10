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

EXPERIMENT: does it improve things when I pass in whose turn it is (1 for X, 0 for O)
At this point, in each game the agent is either randomly X or O.

WHEN I DO PASS THAT IN:

round 0
random opponent: mean reward: -0.48, std reward 9.988473356824857
round 1
random opponent: mean reward: 4.4, std reward 8.968834929911464
last opponent: mean reward: 2.66, std reward 9.629350964628925
round 2
random opponent: mean reward: 9.32, std reward 3.5689774445910976
last opponent: mean reward: 3.46, std reward 9.318175787137738
round 3
random opponent: mean reward: 9.54, std reward 2.9645235704915547
last opponent: mean reward: 6.0, std reward 7.874007874011811
round 4
random opponent: mean reward: 9.63, std reward 2.6005960855157815
last opponent: mean reward: 4.98, std reward 8.579020923159005
round 5
random opponent: mean reward: 8.87, std reward 4.541266343213091
last opponent: mean reward: 3.6, std reward 8.867919710958146
round 6
random opponent: mean reward: 9.56, std reward 2.933666647729425
last opponent: mean reward: 3.36, std reward 9.301096709528398
round 7
random opponent: mean reward: 8.79, std reward 4.757720042205091
last opponent: mean reward: 4.19, std reward 8.703097149865673
round 8
random opponent: mean reward: 8.36, std reward 5.432347558836787
last opponent: mean reward: 2.42, std reward 9.567841971939128
round 9
random opponent: mean reward: 9.36, std reward 3.462715697252664
last opponent: mean reward: 4.69, std reward 8.018971255716036

SAME CODE, WHEN I DON'T PASS THAT IN:

round 0
random opponent: mean reward: 4.76, std reward 8.79445279707612
round 1
random opponent: mean reward: 6.12, std reward 7.895922998611372
last opponent: mean reward: 0.57, std reward 9.968706034385805
round 2
random opponent: mean reward: 9.51, std reward 3.043008379876729
last opponent: mean reward: 4.25, std reward 8.799857953399021
round 3
random opponent: mean reward: 9.62, std reward 2.693622096731463
last opponent: mean reward: 3.95, std reward 8.983178724705414
round 4
random opponent: mean reward: 8.93, std reward 4.4671131617634225
last opponent: mean reward: 2.77, std reward 9.296617664505732
round 5
random opponent: mean reward: 9.36, std reward 3.433715189120962
last opponent: mean reward: 4.6, std reward 8.581375181169975
round 6
random opponent: mean reward: 9.0, std reward 4.312771730569565
last opponent: mean reward: 3.44, std reward 9.282585846627004
round 7
random opponent: mean reward: 9.29, std reward 3.6872618567169866
last opponent: mean reward: 3.74, std reward 9.209364798942433
round 8
random opponent: mean reward: 8.44, std reward 5.344754437764189
last opponent: mean reward: 2.26, std reward 9.73100200390484
round 9
random opponent: mean reward: 8.82, std reward 4.691225852589065
last opponent: mean reward: 4.11, std reward 9.011542598245875


First three rounds of training when we use separate array for X and O:

round 0
random opponent: mean reward: 6.62, std reward 7.495038358807779
round 1
random opponent: mean reward: 9.28, std reward 3.7258019271024057
last opponent: mean reward: 4.73, std reward 8.782203595909174
round 2
random opponent: mean reward: 8.98, std reward 4.399954545219756
last opponent: mean reward: 4.45, std reward 8.916137055922816

----

round 0
random opponent: mean reward: 1.14, std reward 9.934807496876827
round 1
random opponent: mean reward: 9.66, std reward 2.5854206620973685
last opponent: mean reward: 7.27, std reward 6.829868227132937
round 2
random opponent: mean reward: 9.61, std reward 2.7473441721051266
last opponent: mean reward: 5.41, std reward 8.344573086743264

When we don't:

round 0
random opponent: mean reward: 8.27, std reward 5.595274792179558
round 1
random opponent: mean reward: 7.83, std reward 6.212173532669542
last opponent: mean reward: 6.98, std reward 7.132993761387992
round 2
random opponent: mean reward: 8.54, std reward 5.164145621494421
last opponent: mean reward: 4.24, std reward 9.001244358420672

---

round 0
random opponent: mean reward: 7.44, std reward 6.681796165702752
round 1
random opponent: mean reward: 8.17, std reward 5.7576991932541945
last opponent: mean reward: 4.22, std reward 8.99953332123394
round 2
random opponent: mean reward: 9.06, std reward 4.137197118823323
last opponent: mean reward: 4.49, std reward 8.828357718171597

AGENT MAKES AN ILLEGAL MOVE WHEN IT KNOWS ITS GOING TO LOSE:

GAME 0:
step 0:
. . X
. O .
. . .
---
step 1:
. X X
. O O
. . .
---
step 2:
O made an illegal move




-----

0: ELO 814.018430791166, mean reward vs. random player: 9.16, games played: 35747.0
1: ELO 969.3258710741269, mean reward vs. random player: 9.1, games played: 35584.0
3: ELO 868.3242476847793, mean reward vs. random player: 8.7, games played: 33298.0
4: ELO 940.3572374211278, mean reward vs. random player: 7.9, games played: 34812.0
5: ELO 851.6115543528254, mean reward vs. random player: 8.36, games played: 32684.0
6: ELO 925.0103017601375, mean reward vs. random player: 7.28, games played: 35100.0
7: ELO 754.5441785126118, mean reward vs. random player: 7.94, games played: 34252.0
8: ELO 977.9711962597112, mean reward vs. random player: 7.78, games played: 30580.0
10: ELO 748.1163560897344, mean reward vs. random player: 9.26, games played: 33129.0
11: ELO 811.0723534836602, mean reward vs. random player: 8.26, games played: 35692.0
12: ELO 837.6655254326932, mean reward vs. random player: 8.9, games played: 35237.0
13: ELO 912.6010728017847, mean reward vs. random player: 8.58, games played: 33733.0
14: ELO 808.3897116208084, mean reward vs. random player: 9.14, games played: 34117.0
15: ELO 1049.726033560164, mean reward vs. random player: 8.18, games played: 34769.0
16: ELO 924.7260079376642, mean reward vs. random player: 8.94, games played: 32904.0
17: ELO 824.9298210829738, mean reward vs. random player: 8.76, games played: 33083.0
18: ELO 795.0783187578061, mean reward vs. random player: 7.8, games played: 34773.0
19: ELO 1030.605126859194, mean reward vs. random player: 6.98, games played: 32208.0
22: ELO 380.7631379547427, mean reward vs. random player: -15.32, games played: 5156.0
23: ELO 448.3887835821865, mean reward vs. random player: -7.84, games played: 5218.0
