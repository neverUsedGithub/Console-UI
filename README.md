# Console UI

A library for creating console user interfaces.

# Usage
```python
# "Hello, World!" app
from console_ui import text

@app()
def main():
    return (
        text("Hello, World!")
    )
```
```python
# Counter app
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