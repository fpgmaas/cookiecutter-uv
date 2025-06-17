# Evaluation

Evaluate trained models on test datasets using PyTorch Lightning's evaluation capabilities.

## Basic Evaluation

### Evaluate Latest Checkpoint

Evaluate the most recent checkpoint:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.eval
```

This automatically finds and loads the best checkpoint from your latest training run.

### Evaluate Specific Checkpoint

Evaluate a specific checkpoint file:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.eval ckpt_path="/path/to/checkpoint.ckpt"
```

### Evaluate with Custom Data

Override the default test dataset:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.eval data.test_path="/path/to/test/data"
```

## Hardware Configuration

### CPU Evaluation

Force CPU evaluation:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.eval trainer.accelerator=cpu
```

### GPU Evaluation

Use GPU for faster evaluation:

```bash
# Single GPU (automatic if available)
uv run python -m {{cookiecutter.project_slug}}.scripts.eval

# Specify GPU device
uv run python -m {{cookiecutter.project_slug}}.scripts.eval trainer.devices=1 trainer.accelerator=gpu
```

### Multi-GPU Evaluation

Distribute evaluation across multiple GPUs:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.eval trainer.devices=4 trainer.strategy=ddp
```

## Evaluation Outputs

### Results Logging

Evaluation results are automatically saved to:

- **Console**: Immediate results display
- **CSV Files**: Detailed metrics in `logs/eval/` (when CSV logger is configured)
- **TensorBoard**: Visual metrics in tensorboard logs (when TensorBoard logger is configured)
- **Weights & Biases**: Remote experiment tracking (when wandb logger is configured)
- **Comet**: ML experiment tracking and monitoring (when Comet logger is configured)
- **Neptune**: ML experiment management (when Neptune logger is configured)
- **MLflow**: Experiment tracking dashboard (when MLflow logger is configured)


### Batch Size Optimization

Optimize batch size for evaluation speed:

```bash
# Larger batch for faster evaluation
uv run python -m {{cookiecutter.project_slug}}.scripts.eval data.batch_size=128

# Smaller batch if memory constrained
uv run python -m {{cookiecutter.project_slug}}.scripts.eval data.batch_size=32
```

## Debugging Evaluation

### Verbose Output

Enable detailed logging during evaluation:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.eval trainer.logger.level=DEBUG
```

### Limit Evaluation Batches

Quick evaluation for debugging:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.eval debug=limit
```

### Profile Evaluation

Profile evaluation performance:

```bash
uv run python -m {{cookiecutter.project_slug}}.scripts.eval debug=profiler
```

## Troubleshooting

### Memory Issues

If evaluation runs out of memory:

```bash
# Reduce batch size
uv run python -m {{cookiecutter.project_slug}}.scripts.eval data.batch_size=16

# Use CPU evaluation
uv run python -m {{cookiecutter.project_slug}}.scripts.eval trainer.accelerator=cpu

# Use lower precision
uv run python -m {{cookiecutter.project_slug}}.scripts.eval ++trainer.precision=16-mixed
```

### Checkpoint Loading Issues

If checkpoint fails to load:

```bash
# Check checkpoint path
uv run python -m {{cookiecutter.project_slug}}.scripts.eval ckpt_path="/absolute/path/to/checkpoint.ckpt"

# Check checkpoint dict
uv run python -c "import torch; ckpt = torch.load('path/to/checkpoint.ckpt', map_location='cpu'); print('Checkpoint keys:', list(ckpt.keys()))"
```

### Slow Evaluation

Speed up evaluation:

```bash
# Increase data loading workers
uv run python -m {{cookiecutter.project_slug}}.scripts.eval data.num_workers=8

# Enable pin memory
uv run python -m {{cookiecutter.project_slug}}.scripts.eval data.pin_memory=true

# Use compiled model
uv run python -m {{cookiecutter.project_slug}}.scripts.eval model.torch_compile=true
```
