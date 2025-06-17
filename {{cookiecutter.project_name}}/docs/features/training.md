# Training

This guide covers how to train models using the PyTorch Lightning framework with Hydra configuration management.

## Basic Training

### Quick Start

To start training with default configuration:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train
```

This will use the default configuration defined in your project's config files.

### Training with Experiment Configs

It is recommended to use predefined experiment configurations for reproducible training setups and run the experiment with
`experiment=new-defined-one`.

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




### Training with Custom Parameters

You can override any configuration parameter directly from the command line:

```bash
# Change learning rate and batch size
uv run python -m {{cookiecutter.project_slug}}.scripts.train model.optimizer.lr=0.001 data.batch_size=64

# Train for specific number of epochs
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer.max_epochs=50

# Use different model architecture
uv run python -m {{cookiecutter.project_slug}}.scripts.train model=mnist
```

## Hardware Configuration

### GPU Training

PyTorch Lightning automatically detects and uses available GPUs:

```bash
# Single GPU training (automatic)
uv run python -m {{cookiecutter.project_slug}}.scripts.train

# Specify number of GPUs
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer.devices=2

# Multi-GPU training with specific strategy
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer.devices=4 trainer.strategy=ddp
```

### CPU Training

Force CPU training:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer.accelerator=cpu
```

### Mixed Precision Training

Enable automatic mixed precision for faster training:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer.precision=16-mixed
```

## Advanced Training Options

### Resume Training

Resume from a checkpoint:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train ckpt_path="/path/to/checkpoint.ckpt"
```

### Training with Different Experiments

Use predefined experiment configurations:

```bash
# Use specific experiment config
uv run python -m {{cookiecutter.project_slug}}.scripts.train experiment=mnist_experiment

# Override experiment parameters
uv run python -m {{cookiecutter.project_slug}}.scripts.train experiment=mnist_experiment model.optimizer.lr=0.01
```

### Logging and Monitoring

#### TensorBoard (Default)

TensorBoard logs are automatically saved. View them with:

```bash
tensorboard --logdir logs/
```

#### Weights & Biases

If configured, enable W&B logging:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train logger=wandb
```

#### Multiple Loggers

Use multiple loggers simultaneously:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train logger=many_loggers
```

## Training Strategies

### Single Machine Training

```bash
# Standard single GPU
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer.devices=1

# Single machine, multiple GPUs
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer=ddp trainer.devices=4
```

### Distributed Training

For multi-node training, 2 nodes, 4 gpu in each node

```bash
export MASTER_PORT=1234
export MASTER_ADDR=$MASTER_ADDR
export WORLD_SIZE=$NUM_NODES
export NODE_RANK=$NODE_RANK

# Node 0 (master)
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer.devices=4 trainer.num_nodes=$NUM_NODES

# Node 1
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer.devices=4 trainer.num_nodes=$NUM_NODES
```

## Model Checkpointing

### Automatic Checkpointing

The framework automatically saves checkpoints based on validation metrics:

```bash
# Save top 3 models based on validation accuracy
uv run python -m {{cookiecutter.project_slug}}.scripts.train callbacks.model_checkpoint.save_top_k=3 \
                   callbacks.model_checkpoint.monitor="val/acc"
```

### Manual Checkpointing

Save checkpoints at regular intervals:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train callbacks.model_checkpoint.every_n_epochs=10
```

## Training Monitoring

### Progress Bars

Customize training progress display:

```bash
# change different progress bar
uv run python -m {{cookiecutter.project_slug}}.scripts.train callback.progress_bar=rich
```

### Early Stopping

Enable early stopping to prevent overfitting:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train callbacks.early_stopping.monitor="val/loss" \
                   callbacks.early_stopping.patience=10 \
                   callbacks.early_stopping.mode="min"
```

## Common Training Workflows

### Development Training

Quick training for development and debugging:

```bash
# limit training data
uv run python -m {{cookiecutter.project_slug}}.scripts.train debug=limit
```

### Production Training

Full training with all features enabled:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train \
  trainer.max_epochs=100 \
  trainer=ddp \
  trainer.devices=4 \
  trainer.precision=16-mixed \
  callbacks.model_checkpoint.save_top_k=5 \
  callbacks.early_stopping.patience=15
```

### Hyperparameter Tuning

Use Hydra's multirun feature for hyperparameter sweeps:

```bash
# Grid search over learning rates
uv run python -m {{cookiecutter.project_slug}}.scripts.train -m model.optimizer.lr=0.001,0.01,0.1

# Random search with Optuna
uv run python -m {{cookiecutter.project_slug}}.scripts.train -m hparams_search=optuna experiment=example
```

## Debugging Training

### Debug Mode

Enable debug mode for detailed logging:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train debug=default
```

### Profiling

Profile your training code:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train debug=profiler trainer.profiler=simple

# Advanced profiling
uv run python -m {{cookiecutter.project_slug}}.scripts.train debug=profiler trainer.profiler=advanced
```

### Detect Anomalies

Enable anomaly detection:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.train trainer.detect_anomaly=true
```

## Troubleshooting

### Out of Memory (OOM)

- Reduce batch size: `data.batch_size=16`
- Use mixed precision: `trainer.precision=16-mixed`

### Slow Training

- Increase number of workers: `data.num_workers=8`
- Use faster data loading: `data.pin_memory=true`
- Enable compiled model: `model.compile=true`

### Unstable Training

- Reduce learning rate: `model.optimizer.lr=0.0001`
- Add gradient clipping: `trainer.gradient_clip_val=0.5`
- Use learning rate scheduler: `model.scheduler.step_size=30`
