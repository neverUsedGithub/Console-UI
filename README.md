# Console UI

A library for creating console user interfaces.

# Installation

```bash
pip install --use-pep517 git+https://github.com/neverUsedGithub/Console-UI.git
```

# Usage
### "Hello, World!" app
```python
from console_ui import text

@app()
def main(ctx):
    return (
        text("Hello, World!")
    )
```
### Counter App
```python
from console_ui import text, on_key

@app(
    state = {
        "count": 0
    }
)
def main(ctx):
    @on_key()
    def pressed(key):
        ctx["count"].set(lambda count: count + 1)
    
    return (
        text("Count is ", ctx["count"])
    )
```