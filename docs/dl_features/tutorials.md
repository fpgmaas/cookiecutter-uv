# Hydra Configuration

This project uses [Hydra](https://hydra.cc/) for flexible and composable configuration management, enabling organized and reproducible machine learning experiments.

## How It Works

All PyTorch Lightning modules are dynamically instantiated from module paths specified in config. Example model config:

```yaml
_target_: src.models.mnist_model.MNISTLitModule
lr: 0.001
net:
  _target_: src.models.components.simple_dense_net.SimpleDenseNet
  input_size: 784
  lin1_size: 256
  lin2_size: 256
  lin3_size: 256
  output_size: 10
```

Using this config we can instantiate the object with the following line:

```python
model = hydra.utils.instantiate(config.model)
```

This allows you to easily iterate over new models! Every time you create a new one, just specify its module path and parameters in appropriate config file. <br>

Switch between models and datamodules with command line arguments:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train model=mnist
```

Example pipeline managing the instantiation logic: [scripts/train.py](https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/blob/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/scripts/train.py).

<br>

## Main Config

Location: [configs/train.yaml]https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/configs/train.yaml) <br>
Main project config contains default training configuration.<br>
It determines how config is composed when simply executing command `uv run python -m {{cookiecutter.project_slug}}.scripts.train`.<br>

<details>
<summary><b>Show main project config</b></summary>

```yaml
# order of defaults determines the order in which configs override each other
defaults:
  - _self_
  - data: mnist.yaml
  - model: mnist.yaml
  - callbacks: default.yaml
  - logger: null # set logger here or use command line (e.g. `uv run python -m {{cookiecutter.project_slug}}.scripts.train logger=csv`)
  - trainer: default.yaml
  - paths: default.yaml
  - extras: default.yaml
  - hydra: default.yaml

  # experiment configs allow for version control of specific hyperparameters
  # e.g. best hyperparameters for given model and datamodule
  - experiment: null

  # config for hyperparameter optimization
  - hparams_search: null

  # optional local config for machine/user specific settings
  # it's optional since it doesn't need to exist and is excluded from version control
  - optional local: default.yaml

  # debugging config (enable through command line, e.g. `uv run python -m {{cookiecutter.project_slug}}.scripts.train debug=default)
  - debug: null

# task name, determines output directory path
task_name: "train"

# tags to help you identify your experiments
# you can overwrite this in experiment configs
# overwrite from command line with `uv run python -m {{cookiecutter.project_slug}}.scripts.train tags="[first_tag, second_tag]"`
# appending lists from command line is currently not supported :(
# https://github.com/facebookresearch/hydra/issues/1547
tags: ["dev"]

# set False to skip model training
train: True

# evaluate on test set, using best model weights achieved during training
# lightning chooses best weights based on the metric specified in checkpoint callback
test: True

# simply provide checkpoint path to resume training
ckpt_path: null

# seed for random number generators in pytorch, numpy and python.random
seed: null
```

</details>

<br>

## Experiment Config

Location: [configs/experiment]https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/configs/experiment)<br>
Experiment configs allow you to overwrite parameters from main config.<br>
For example, you can use them to version control best hyperparameters for each combination of model and dataset.

<details>
<summary><b>Show example experiment config</b></summary>

```yaml
# @package _global_

# to execute this experiment run:
# uv run python -m {{cookiecutter.project_slug}}.scripts.train experiment=example

defaults:
  - override /data: mnist.yaml
  - override /model: mnist.yaml
  - override /callbacks: default.yaml
  - override /trainer: default.yaml

# all parameters below will be merged with parameters from default configurations set above
# this allows you to overwrite only specified parameters

tags: ["mnist", "simple_dense_net"]

seed: 12345

trainer:
  min_epochs: 10
  max_epochs: 10
  gradient_clip_val: 0.5

model:
  optimizer:
    lr: 0.002
  net:
    lin1_size: 128
    lin2_size: 256
    lin3_size: 64

data:
  batch_size: 64

logger:
  wandb:
    tags: ${tags}
    group: "mnist"
```

</details>

<br>

## Workflow

**Basic workflow**

1. Write your PyTorch Lightning module (see [models/mnist_module.py](https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/models/mnist_module.py) for example)
2. Write your PyTorch Lightning datamodule (see [data/mnist_datamodule.py](https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/data/mnist_datamodule.py) for example)
3. Write your experiment config, containing paths to model and datamodule
4. Run training with chosen experiment config:
   ```bash
   uv run python -m {{cookiecutter.project_slug}}.scripts.train experiment=experiment_name.yaml
   ```

**Experiment design**

_Say you want to execute many runs to plot how accuracy changes in respect to batch size._

1. Execute the runs with some config parameter that allows you to identify them easily, like tags:

   ```bash
   uv run python -m {{cookiecutter.project_slug}}.scripts.train -m logger=csv data.batch_size=16,32,64,128 tags=["batch_size_exp"]
   ```

2. Write a script or notebook that searches over the `logs/` folder and retrieves csv logs from runs containing given tags in config. Plot the results.

<br>

## Logs

Hydra creates new output directory for every executed run.

Default logging structure:

```
├── logs
│   ├── task_name
│   │   ├── runs                        # Logs generated by single runs
│   │   │   ├── YYYY-MM-DD_HH-MM-SS       # Datetime of the run
│   │   │   │   ├── .hydra                  # Hydra logs
│   │   │   │   ├── csv                     # Csv logs
│   │   │   │   ├── wandb                   # Weights&Biases logs
│   │   │   │   ├── checkpoints             # Training checkpoints
│   │   │   │   └── ...                     # Any other thing saved during training
│   │   │   └── ...
│   │   │
│   │   └── multiruns                   # Logs generated by multiruns
│   │       ├── YYYY-MM-DD_HH-MM-SS       # Datetime of the multirun
│   │       │   ├──1                        # Multirun job number
│   │       │   ├──2
│   │       │   └── ...
│   │       └── ...
│   │
│   └── debugs                          # Logs generated when debugging config is attached
│       └── ...
```

</details>

You can change this structure by modifying paths in [hydra configuration](https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/hydra).

<br>

## Experiment Tracking

PyTorch Lightning supports many popular logging frameworks: [Weights&Biases](https://www.wandb.com/), [Neptune](https://neptune.ai/), [Comet](https://www.comet.ml/), [MLFlow](https://mlflow.org), [Tensorboard](https://www.tensorflow.org/tensorboard/).

These tools help you keep track of hyperparameters and output metrics and allow you to compare and visualize results. To use one of them simply complete its configuration in [configs/logger]https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/configs/logger) and run:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train logger=logger_name
```

You can use many of them at once (see [configs/logger/many_loggers.yaml]https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/configs/logger/many_loggers.yaml) for example).

You can also write your own logger.

Lightning provides convenient method for logging custom metrics from inside LightningModule. Read the [docs](https://pytorch-lightning.readthedocs.io/en/latest/extensions/logging.html#automatic-logging) or take a look at [MNIST example](https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/models/mnist_module.py).

<br>

## Tests

Template comes with generic tests implemented with `pytest`.

```bash
# run all tests
make test
```

Most of the implemented tests don't check for any specific output - they exist to simply verify that executing some commands doesn't end up in throwing exceptions. You can execute them once in a while to speed up the development.

Currently, the tests cover cases like:

- running 1 train, val and test step
- running 1 epoch on 1% of data, saving ckpt and resuming for the second epoch
- running 2 epochs on 1% of data, with DDP simulated on CPU

And many others. You should be able to modify them easily for your use case.

There is also `@RunIf` decorator implemented, that allows you to run tests only if certain conditions are met, e.g. GPU is available or system is not windows. See the [examples](https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/tests/test_train.py).

<br>

## Hyperparameter Search

You can define hyperparameter search by adding new config file to [configs/hparams_search]https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/configs/hparams_search).

<details>
<summary><b>Show example hyperparameter search config</b></summary>

```yaml
# @package _global_

defaults:
  - override /hydra/sweeper: optuna

# choose metric which will be optimized by Optuna
# make sure this is the correct name of some metric logged in lightning module!
optimized_metric: "val/acc_best"

# here we define Optuna hyperparameter search
# it optimizes for value returned from function with @hydra.main decorator
hydra:
  sweeper:
    _target_: hydra_plugins.hydra_optuna_sweeper.optuna_sweeper.OptunaSweeper

    # 'minimize' or 'maximize' the objective
    direction: maximize

    # total number of runs that will be executed
    n_trials: 20

    # choose Optuna hyperparameter sampler
    # docs: https://optuna.readthedocs.io/en/stable/reference/samplers.html
    sampler:
      _target_: optuna.samplers.TPESampler
      seed: 1234
      n_startup_trials: 10 # number of random sampling runs before optimization starts

    # define hyperparameter search space
    params:
      model.optimizer.lr: interval(0.0001, 0.1)
      data.batch_size: choice(32, 64, 128, 256)
      model.net.lin1_size: choice(64, 128, 256)
      model.net.lin2_size: choice(64, 128, 256)
      model.net.lin3_size: choice(32, 64, 128, 256)
```

</details>

Next, execute it with: `uv run python -m {{cookiecutter.project_slug}}.scripts.train -m hparams_search=mnist_optuna`

Using this approach doesn't require adding any boilerplate to code, everything is defined in a single config file. The only necessary thing is to return the optimized metric value from the launch file.

You can use different optimization frameworks integrated with Hydra, like [Optuna, Ax or Nevergrad](https://hydra.cc/docs/plugins/optuna_sweeper/).

The `optimization_results.yaml` will be available under `logs/task_name/multirun` folder.

This approach doesn't support resuming interrupted search and advanced techniques like prunning - for more sophisticated search and workflows, you should probably write a dedicated optimization task (without multirun feature).

<br>

## Continuous Integration

Template comes with CI workflows implemented in Github Actions:

- `.github/workflows/test.yaml`: running all tests with pytest
- `.github/workflows/code-quality-main.yaml`: running pre-commits on main branch for all files
- `.github/workflows/code-quality-pr.yaml`: running pre-commits on pull requests for modified files only

<br>

## Distributed Training

Lightning supports multiple ways of doing distributed training. The most common one is DDP, which spawns separate process for each GPU and averages gradients between them. To learn about other approaches read the [lightning docs](https://lightning.ai/docs/pytorch/latest/advanced/speed.html).

You can run DDP on mnist example with 4 GPUs like this:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer=ddp
```

> **Note**: When using DDP you have to be careful how you write your models - read the [docs](https://lightning.ai/docs/pytorch/latest/advanced/speed.html).

<br>

## Accessing Datamodule Attributes In Model

The simplest way is to pass datamodule attribute directly to model on initialization:

```python
# ./src/train.py
datamodule = hydra.utils.instantiate(config.data)
model = hydra.utils.instantiate(config.model, some_param=datamodule.some_param)
```

> **Note**: Not a very robust solution, since it assumes all your datamodules have `some_param` attribute available.

Similarly, you can pass a whole datamodule config as an init parameter:

```python
# ./src/train.py
model = hydra.utils.instantiate(config.model, dm_conf=config.data, _recursive_=False)
```

You can also pass a datamodule config parameter to your model through variable interpolation:

```yaml
# ./configs/model/my_model.yaml
_target_: src.models.my_module.MyLitModule
lr: 0.01
some_param: ${data.some_param}
```

Another approach is to access datamodule in LightningModule directly through Trainer:

```python
# ./src/models/mnist_module.py
def on_train_start(self):
  self.some_param = self.trainer.datamodule.some_param
```

> **Note**: This only works after the training starts since otherwise trainer won't be yet available in LightningModule.

<br>

## Configuration Composition

### Runtime Configuration

Hydra allows you to override any configuration in runtime parameter directly from the command line without modifying config files. This enables flexible experimentation and parameter tuning. using dot notation

```bash
# Use specific experiment configuration
uv run python -m {{cookiecutter.project_slug}}.scripts.train experiment=example

# Override default data
uv run python -m {{cookiecutter.project_slug}}.scripts.train data=mnist

# Override default model
uv run python -m {{cookiecutter.project_slug}}.scripts.train model=mnist

# Override default trainer
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer=gpu

# Override specific parameters
uv run python -m {{cookiecutter.project_slug}}.scripts.train model.optimizer.lr=0.01 data.batch_size=128

# Combine multiple overrides
uv run python -m {{cookiecutter.project_slug}}.scripts.train experiment=example trainer.max_epochs=20 trainer.devices=2
```
