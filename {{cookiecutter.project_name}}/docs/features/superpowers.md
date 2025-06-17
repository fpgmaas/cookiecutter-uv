## Your Superpowers with Hydra

<details>
<summary><b>Override any config parameter from command line</b></summary>

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer.max_epochs=20 model.optimizer.lr=1e-4
```

> **Note**: You can also add new parameters with `+` sign.

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train +model.new_param="owo"
```

</details>

<details>
<summary><b>Train on CPU, GPU, multi-GPU and TPU</b></summary>

```bash
# train on CPU
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer=cpu

# train on 1 GPU
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer=gpu

# train on TPU
uv run python -m {{cookiecutter.project_slug}}.scripts.train +trainer.tpu_cores=8

# train with DDP (Distributed Data Parallel) (4 GPUs)
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer=ddp trainer.devices=4

# train with DDP (Distributed Data Parallel) (8 GPUs, 2 nodes)
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer=ddp trainer.devices=4 trainer.num_nodes=2

# simulate DDP on CPU processes
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer=ddp_sim trainer.devices=2

# accelerate training on mac
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer=mps
```

> **Warning**: Currently there are problems with DDP mode, read [this issue](https://github.com/ashleve/lightning-hydra-template/issues/393) to learn more.

</details>

<details>
<summary><b>Train with mixed precision</b></summary>

```bash
# train with pytorch native automatic mixed precision (AMP)
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer=gpu +trainer.precision=16
```

</details>

<!-- deepspeed support still in beta
<details>
<summary><b>Optimize large scale models on multiple GPUs with Deepspeed</b></summary>

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train +trainer.
```

</details>
 -->

<details>
<summary><b>Train model with any logger available in PyTorch Lightning, like W&B or Tensorboard</b></summary>

```yaml
# set project and entity names in `configs/logger/wandb`
wandb:
  project: "your_project_name"
  entity: "your_wandb_team_name"
```

```bash
# train model with Weights&Biases (link to wandb dashboard should appear in the terminal)
uv run python -m {{cookiecutter.project_slug}}.scripts.train logger=wandb
```

> **Note**: Lightning provides convenient integrations with most popular logging frameworks. Learn more [here](#experiment-tracking).

> **Note**: Using wandb requires you to [setup account](https://www.wandb.com/) first. After that just complete the config as below.

> **Note**: Click [here](https://wandb.ai/hobglob/template-dashboard/) to see example wandb dashboard generated with this template.

</details>

<details>
<summary><b>Train model with chosen experiment config</b></summary>

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train experiment=example
```

> **Note**: Experiment configs are placed in [configs/experiment/]https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/configs/experiment/).

</details>

<details>
<summary><b>Attach some callbacks to run</b></summary>

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train callbacks=default
```

> **Note**: Callbacks can be used for things such as as model checkpointing, early stopping and [many more](https://pytorch-lightning.readthedocs.io/en/latest/extensions/callbacks.html#built-in-callbacks).

> **Note**: Callbacks configs are placed in [configs/callbacks/]https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/configs/callbacks/).

</details>

<details>
<summary><b>Use different tricks available in Pytorch Lightning</b></summary>

```yaml
# gradient clipping may be enabled to avoid exploding gradients
uv run python -m {{cookiecutter.project_slug}}.scripts.train +trainer.gradient_clip_val=0.5

# run validation loop 4 times during a training epoch
uv run python -m {{cookiecutter.project_slug}}.scripts.train +trainer.val_check_interval=0.25

# accumulate gradients
uv run python -m {{cookiecutter.project_slug}}.scripts.train +trainer.accumulate_grad_batches=10

# terminate training after 12 hours
uv run python -m {{cookiecutter.project_slug}}.scripts.train +trainer.max_time="00:12:00:00"
```

> **Note**: PyTorch Lightning provides about [40+ useful trainer flags](https://pytorch-lightning.readthedocs.io/en/latest/common/trainer.html#trainer-flags).

</details>

<details>
<summary><b>Easily debug</b></summary>

```bash
# runs 1 epoch in default debugging mode
# changes logging directory to `logs/debugs/...`
# sets level of all command line loggers to 'DEBUG'
# enforces debug-friendly configuration
uv run python -m {{cookiecutter.project_slug}}.scripts.train debug=default

# run 1 train, val and test loop, using only 1 batch
uv run python -m {{cookiecutter.project_slug}}.scripts.train debug=fdr

# print execution time profiling
uv run python -m {{cookiecutter.project_slug}}.scripts.train debug=profiler

# try overfitting to 1 batch
uv run python -m {{cookiecutter.project_slug}}.scripts.train debug=overfit

# raise exception if there are any numerical anomalies in tensors, like NaN or +/-inf
uv run python -m {{cookiecutter.project_slug}}.scripts.train +trainer.detect_anomaly=true

# use only 20% of the data
uv run python -m {{cookiecutter.project_slug}}.scripts.train +trainer.limit_train_batches=0.2 \
+trainer.limit_val_batches=0.2 +trainer.limit_test_batches=0.2
```

> **Note**: Visit [configs/debug/]https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/configs/debug/) for different debugging configs.

</details>

<details>
<summary><b>Resume training from checkpoint</b></summary>

```yaml
uv run python -m {{cookiecutter.project_slug}}.scripts.train ckpt_path="/path/to/ckpt/name.ckpt"
```

> **Note**: Checkpoint can be either path or URL.

> **Note**: Currently loading ckpt doesn't resume logger experiment, but it will be supported in future Lightning release.

</details>

<details>
<summary><b>Evaluate checkpoint on test dataset</b></summary>

```yaml
uv run python -m {{cookiecutter.project_slug}}.scripts.eval ckpt_path="/path/to/ckpt/name.ckpt"
```

> **Note**: Checkpoint can be either path or URL.

</details>

<details>
<summary><b>Create a sweep over hyperparameters</b></summary>

```bash
# this will run 6 experiments one after the other,
# each with different combination of batch_size and learning rate
uv run python -m {{cookiecutter.project_slug}}.scripts.train -m data.batch_size=32,64,128 model.lr=0.001,0.0005
```

> **Note**: Hydra composes configs lazily at job launch time. If you change code or configs after launching a job/sweep, the final composed configs might be impacted.

</details>

<details>
<summary><b>Create a sweep over hyperparameters with Optuna</b></summary>

```bash
# this will run hyperparameter search defined in `configs/hparams_search/mnist_optuna.yaml`
# over chosen experiment config
uv run python -m {{cookiecutter.project_slug}}.scripts.train -m hparams_search=mnist_optuna experiment=example
```

> **Note**: Using [Optuna Sweeper](https://hydra.cc/docs/next/plugins/optuna_sweeper) doesn't require you to add any boilerplate to your code, everything is defined in a [single config file]https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/configs/hparams_search/mnist_optuna.yaml).

> **Warning**: Optuna sweeps are not failure-resistant (if one job crashes then the whole sweep crashes).

</details>

<details>
<summary><b>Execute all experiments from folder</b></summary>

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train -m 'experiment=glob(*)'
```

> **Note**: Hydra provides special syntax for controlling behavior of multiruns. Learn more [here](https://hydra.cc/docs/next/tutorials/basic/running_your_app/multi-run). The command above executes all experiments from [configs/experiment/]https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/tree/main/{{cookiecutter.project_name}}/{{cookiecutter.project_slug}}/configs/experiment/).

</details>

<details>
<summary><b>Execute run for multiple different seeds</b></summary>

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train -m seed=1,2,3,4,5 trainer.deterministic=True logger=csv tags=["benchmark"]
```

> **Note**: `trainer.deterministic=True` makes pytorch more deterministic but impacts the performance.

</details>

<details>
<summary><b>Execute sweep on a remote AWS cluster</b></summary>

> **Note**: This should be achievable with simple config using [Ray AWS launcher for Hydra](https://hydra.cc/docs/next/plugins/ray_launcher). Example is not implemented in this template.

</details>

<!-- <details>
<summary><b>Execute sweep on a SLURM cluster</b></summary>

> This should be achievable with either [the right lightning trainer flags](https://pytorch-lightning.readthedocs.io/en/latest/clouds/cluster.html?highlight=SLURM#slurm-managed-cluster) or simple config using [Submitit launcher for Hydra](https://hydra.cc/docs/plugins/submitit_launcher). Example is not yet implemented in this template.

</details> -->

<details>
<summary><b>Use Hydra tab completion</b></summary>

> **Note**: Hydra allows you to autocomplete config argument overrides in shell as you write them, by pressing `tab` key. Read the [docs](https://hydra.cc/docs/tutorials/basic/running_your_app/tab_completion).

</details>

<details>
<summary><b>Apply pre-commit hooks</b></summary>

```bash
pre-commit run -a
```

> **Note**: Apply pre-commit hooks to do things like auto-formatting code and configs, performing code analysis or removing output from jupyter notebooks. See [# Best Practices](#best-practices) for more.

Update pre-commit hook versions in `.pre-commit-config.yaml` with:

```bash
pre-commit autoupdate
```

</details>

<details>
<summary><b>Run tests</b></summary>

```bash
# run all tests
pytest

# run tests from specific file
pytest tests/test_train.py

# run all tests except the ones marked as slow
pytest -k "not slow"
```

</details>

<details>
<summary><b>Use tags</b></summary>

Each experiment should be tagged in order to easily filter them across files or in logger UI:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train tags=["mnist","experiment_X"]
```

> **Note**: You might need to escape the bracket characters in your shell with `uv run python -m {{cookiecutter.project_slug}}.scripts.train tags=\["mnist","experiment_X"\]`.

If no tags are provided, you will be asked to input them from command line:

```bash
>>> uv run python -m {{cookiecutter.project_slug}}.scripts.train tags=[]
[2022-07-11 15:40:09,358][src.utils.utils][INFO] - Enforcing tags! <cfg.extras.enforce_tags=True>
[2022-07-11 15:40:09,359][src.utils.rich_utils][WARNING] - No tags provided in config. Prompting user to input tags...
Enter a list of comma separated tags (dev):
```

If no tags are provided for multirun, an error will be raised:

```bash
>>> uv run python -m {{cookiecutter.project_slug}}.scripts.train -m +x=1,2,3 tags=[]
ValueError: Specify tags before launching a multirun!
```

> **Note**: Appending lists from command line is currently not supported in hydra :(

</details>
