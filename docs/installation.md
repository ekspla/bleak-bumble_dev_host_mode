# Installation

To install `bleak_bumble` of this fork, you need to install it along with its dependencies.

## Requirements

- Python >= 3.10
- bleak == 3.0.1
- bumble == 0.0.227

## Installation Options

### Via pip (Not available from PyPI at the moment)

```bash
pip install -e git+https://github.com/ekspla/bleak-bumble_dev_host_mode.git#egg=bleak_bumble
```

### Development Installation

To install for development, `git clone` or download an archive from GitHub.  

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
