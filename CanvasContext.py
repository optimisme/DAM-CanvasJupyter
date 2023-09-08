from IPython.display import display, HTML, Javascript

class CanvasContext:

    DATA = {}

    PROPERTIES = {
        "lineWidth": {"type": "number", "default": 1.0},
        "lineCap": {"type": "string", "default": "butt"},  # butt, round, square
        "lineJoin": {"type": "string", "default": "miter"},  # miter, round, bevel
        "miterLimit": {"type": "number", "default": 10.0},
        "lineDashOffset": {"type": "number", "default": 0.0},
        "font": {"type": "string", "default": "10px sans-serif"},
        "textAlign": {"type": "string", "default": "start"},  # start, end, left, right, center
        "textBaseLine": {"type": "string", "default": "alphabetic"},  # alphabetic, top, hanging, middle, ideographic, bottom
        "direction": {"type": "string", "default": "inherit"},  # ltr, rtl, inherit
        "letterSpacing": {"type": "number", "default": 0},
        "fontKerning": {"type": "string", "default": "auto"},  # auto, normal, none
        "wordSpacing": {"type": "number", "default": 0},
        "fillStyle": {"type": "string", "default": "blue"},
        "strokeStyle": {"type": "string", "default": "black"},
        "shadowBlur": {"type": "number", "default": 0},
        "shadowColor": {"type": "string", "default": "transparent black"},
        "shadowOffsetX": {"type": "number", "default": 0},
        "shadowOffsetY": {"type": "number", "default": 0},
        "globalAlpha": {"type": "number", "default": 1.0},
        "isSmoothingEnabled": {"type": "boolean", "default": True},
        "globalCompositeOperation": {"type": "string", "default": "source-over"},  # Hi ha molts valors possibles, source-over és el predeterminat
        "imageSmoothingQuality": {"type": "string", "default": "low"},  # low, medium, high
        "canvas": {"type": "object", "default": None},  # Això pot necessitar una gestió especial segons com es vulgui utilitzar
        "filter": {"type": "string", "default": "none"}  # none, blur(), brightness(), etc.
    }

    def __init__(self, canvas_id, ample=400, alt=400):
        self.canvas_id = canvas_id
        for prop, meta in self.PROPERTIES.items():
            setattr(self, f"_{prop}", meta["default"])  # Inicialitzem amb el valor per defecte
        display(HTML(f"""<canvas id="{self.canvas_id}" width="{ample}" height="{alt}" style="border:1px solid black;"></canvas>"""))
        self._defineGetContextFunction()

    def _defineGetContextFunction(self):
        js_code = f"""
        window.getContext_{self.canvas_id} = function() {{
            var canvas = document.getElementById('{self.canvas_id}');
            return canvas.getContext('2d');
        }};
        """
        display(Javascript(js_code))

    def _set_property(self, prop_name, value):
        meta = self.PROPERTIES[prop_name]
        if meta["type"] == "string":
            value = f"'{value}'"
        elif meta["type"] == "number":
            value = str(value)  # Convertim el número a string per a la interpolació
        # Si es necessiten altres conversions de tipus, es poden afegir aquí

        setattr(self, f"_{prop_name}", value)
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.{prop_name} = {value};
        """
        display(Javascript(js_code))

    def _get_property(self, prop_name):
        return getattr(self, f"_{prop_name}")

    def measureText(self, text):
        global DATA
        DATA.clear()  # Neteja les dades antigues

        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        var measure = ctx.measureText('{text}');
        IPython.notebook.kernel.execute('store_data width ' + measure.width);
        """
        display(Javascript(js_code))

        # Espera que es rebin les dades (això pot ser una mica arriesgat ja que podríem entrar en un bucle infinit si no rebem les dades)
        while 'width' not in DATA:
            pass

        return float(DATA['width'])  # Convertim l'amplada a float i la retornem

    def isPointInPath(self, x, y):
        global DATA
        DATA.clear()  # Neteja les dades antigues

        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        var isInPath = ctx.isPointInPath({x}, {y});
        IPython.notebook.kernel.execute('store_data inPath ' + isInPath);
        """
        display(Javascript(js_code))

        # Espera que es rebin les dades
        while 'inPath' not in DATA:
            pass

        return bool(DATA['inPath'])  # Convertim a boolean i retornem

    def isPointInStroke(self, x, y):
        global DATA
        DATA.clear()  # Neteja les dades antigues

        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        var isInStroke = ctx.isPointInStroke({x}, {y});
        IPython.notebook.kernel.execute('store_data inStroke ' + isInStroke);
        """
        display(Javascript(js_code))

        # Espera que es rebin les dades
        while 'inStroke' not in DATA:
            pass

        return bool(DATA['inStroke'])  # Convertim a boolean i retornem

    def getTransform(self):
        global DATA
        DATA.clear()  # Neteja les dades antigues

        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        var transform = ctx.getTransform();
        IPython.notebook.kernel.execute('store_data transform ' + JSON.stringify([transform.a, transform.b, transform.c, transform.d, transform.e, transform.f]));
        """
        display(Javascript(js_code))

        # Espera que es rebin les dades
        while 'transform' not in DATA:
            pass

        return DATA['transform']  # Retorna la llista de transformacions

    def getLineDash(self):
        DATA.clear()  # Neteja les dades antigues

        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        var dashes = ctx.getLineDash();
        IPython.notebook.kernel.execute('store_data("dashes", ' + JSON.stringify(dashes) + ')');
        """
        display(Javascript(js_code))

        # Espera que es rebin les dades (això pot ser una mica arriesgat ja que podríem entrar en un bucle infinit si no rebem les dades)
        while 'dashes' not in DATA:
            pass

        return DATA['dashes']

    def save(self):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.save();
        """
        display(Javascript(js_code))

    def restore(self):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.restore();
        """
        display(Javascript(js_code))

    def rectangle(self, x, y, ample, alt):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.rect({x}, {y}, {ample}, {alt});
        """
        display(Javascript(js_code))

    def fillRect(self, x, y, ample, alt):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.fillRect({x}, {y}, {ample}, {alt});
        """
        display(Javascript(js_code))

    def clearRect(self, x, y, ample, alt):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.clearRect({x}, {y}, {ample}, {alt});
        """
        display(Javascript(js_code))

    def strokeRect(self, x, y, ample, alt):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.strokeRect({x}, {y}, {ample}, {alt});
        """
        display(Javascript(js_code))

    def fillText(self, text, x, y, maxAmple=None):
        maxAmpleStr = f", {maxAmple}" if maxAmple else ""
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.fillText('{text}', {x}, {y}{maxAmpleStr});
        """
        display(Javascript(js_code))

    def strokeText(self, text, x, y, maxAmple=None):
        maxAmpleStr = f", {maxAmple}" if maxAmple else ""
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.strokeText('{text}', {x}, {y}{maxAmpleStr});
        """
        display(Javascript(js_code))

    def beginPath(self):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.beginPath();
        """
        display(Javascript(js_code))

    def closePath(self):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.closePath();
        """
        display(Javascript(js_code))

    def moveTo(self, x, y):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.moveTo({x}, {y});
        """
        display(Javascript(js_code))

    def lineTo(self, x, y):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.lineTo({x}, {y});
        """
        display(Javascript(js_code))

    def bezierCurveTo(self, cp1x, cp1y, cp2x, cp2y, x, y):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.bezierCurveTo({cp1x}, {cp1y}, {cp2x}, {cp2y}, {x}, {y});
        """
        display(Javascript(js_code))

    def quadraticCurveTo(self, cpx, cpy, x, y):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.quadraticCurveTo({cpx}, {cpy}, {x}, {y});
        """
        display(Javascript(js_code))

    def arc(self, x, y, radius, startAngle, endAngle, anticlockwise=False):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.arc({x}, {y}, {radius}, {startAngle}, {endAngle}, {str(anticlockwise).lower()});
        """
        display(Javascript(js_code))

    def arcTo(self, x1, y1, x2, y2, radius):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.arcTo({x1}, {y1}, {x2}, {y2}, {radius});
        """
        display(Javascript(js_code))

    def ellipse(self, x, y, radiusX, radiusY, rotation, startAngle, endAngle, anticlockwise=False):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.ellipse({x}, {y}, {radiusX}, {radiusY}, {rotation}, {startAngle}, {endAngle}, {str(anticlockwise).lower()});
        """
        display(Javascript(js_code))

    def roundRect(self, x, y, width, height, radius):
        # Implementació de rectangle amb cantons arrodonits amb un radi determinat
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.roundRect({x}, {y} , {width}, {height}, {radius});
        """
        display(Javascript(js_code))

    def fill(self):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.fill();
        """
        display(Javascript(js_code))

    def stroke(self):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.stroke();
        """
        display(Javascript(js_code))

    def clip(self):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.clip();
        """
        display(Javascript(js_code))

    def rotate(self, angle):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.rotate({angle});
        """
        display(Javascript(js_code))

    def scale(self, scaleX, scaleY):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.scale({scaleX}, {scaleY});
        """
        display(Javascript(js_code))

    def translate(self, x, y):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.translate({x}, {y});
        """
        display(Javascript(js_code))

    def transform(self, a, b, c, d, e, f):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.transform({a}, {b}, {c}, {d}, {e}, {f});
        """
        display(Javascript(js_code))

    def setTransform(self, a, b, c, d, e, f):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.setTransform({a}, {b}, {c}, {d}, {e}, {f});
        """
        display(Javascript(js_code))

    def resetTransform(self):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.resetTransform();
        """
        display(Javascript(js_code))

    def drawImage(self, source, sx, sy, sWidth, sHeight, dx, dy, dWidth, dHeight):
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        var img = new Image();
        img.src = '{source}';
        img.onload = function() {{
            ctx.drawImage(img, {sx}, {sy}, {sWidth}, {sHeight}, {dx}, {dy}, {dWidth}, {dHeight});
        }};
        """
        display(Javascript(js_code))

    def putImageData(self, imageData, dx, dy):
        # Aquí, imageData hauria de ser una cadena que representi les dades de la imatge
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.putImageData({imageData}, {dx}, {dy});
        """
        display(Javascript(js_code))

    def setLineDash(self, segments):
        # Aquí, `segments` hauria de ser una llista o array de números
        js_code = f"""
        var ctx = window.getContext_{self.canvas_id}();
        ctx.setLineDash([{",".join(map(str, segments))}]);
        """
        display(Javascript(js_code))

for prop in CanvasContext.PROPERTIES.keys():
    getter = lambda self, prop=prop: self._get_property(prop)
    setter = lambda self, value, prop=prop: self._set_property(prop, value)
    setattr(CanvasContext, prop, property(getter, setter))
