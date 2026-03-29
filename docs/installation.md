# Installation

To install `bleak_bumble`, you need to install it along with its dependencies.

## Requirements

- Python >= 3.9
- bleak >= 1.0.0, < 1.1.0
- bumble == 0.0.211

## Installation Options

### Via pip (Not available at the moment)

```bash
pip install bleak_bumble
```

### Development Installation

To install for development:

```bash
git clone https://github.com/vChavezB/bleak-bumble
cd bleak-bumble
pip install -e .
```

### Using Poetry

```bash
poetry install
```

## Verification

To verify your installation, run:

```python
import bleak_bumble
print(f"bleak_bumble version: {bleak_bumble.__version__}")
```
