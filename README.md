# Canvas > Jupyter / Colab

This is a library for calling canvas functions in Jupyter or Google Colab.

Simply add the library named 'CanvasContext.py' to your project folder to use it.

## Example

```python
from CanvasContext import CanvasContext

# Create a canvas with an identifier "cnv" of 500x500 pixels
ctx = CanvasContext("cnv", 500, 300)

# Draw background
ctx.drawGridBackground()

# Draw a filled rectangle in blue (by default) at position (50, 50) with dimensions 200x100
ctx.fillRect(50, 50, 200, 100)

# Set the stroke style to green and draw a rectangle at position (100, 100) with dimensions 200x100
ctx.strokeStyle = "green"
ctx.lineWidth = 5
ctx.strokeRect(100, 100, 200, 100)

# Draw text at position (150, 250)
ctx.font = "26px Arial"
ctx.fillText("Hello, world!", 150, 250)

```