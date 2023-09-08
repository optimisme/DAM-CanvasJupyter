# Canvas > Jupyter / Colab

This is a library to call canvas from Jupyter or Google Colab

Just add the library named 'CanvasContext.py' to the project folder and use it.

## Example

```python
from CanvasContext import CanvasContext

# Crear un canvas amb un identificador "meuCanvas" de 500x500 píxels
canvas = CanvasContext("meuCanvas", 500, 500)

# Dibuixar un rectangle ple de color blau (per defecte) a la posició (50, 50) amb dimensions 200x100
canvas.fillRect(50, 50, 200, 100)

# Establir l'estil del traçat a vermell i dibuixar un rectangle en la posició (100, 100) amb dimensions 200x100
canvas._set_property("strokeStyle", "red")
canvas.strokeRect(100, 100, 200, 100)

# Dibuixar text a la posició (150, 250)
canvas.fillText("Hola, món!", 150, 250)
```