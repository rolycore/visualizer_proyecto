# Visualizer Proyecto — Clasificador de Formas (Círculo vs Cuadrado)

Programa en Python que usa OpenCV para calibrar un "patrón" de circularidad a partir de dos imágenes de referencia (un círculo y un cuadrado) y luego clasifica en tiempo real, usando la cámara, si la figura mostrada es un círculo, un cuadrado, o si el resultado es dudoso.

## Requisitos previos

- Python 3.8 o superior instalado.
- Una cámara web conectada y con permisos habilitados para el sistema/terminal.
- Dos imágenes de referencia:
  - Una foto de un **círculo** oscuro sobre fondo claro (ej. `circulo.jpg`).
  - Una foto de un **cuadrado** oscuro sobre fondo claro (ej. `cuadrado.png`).

Este repositorio ya incluye `circulo.jpg` y `cuadrado.png` como ejemplos que puedes usar directamente.

## Paso a paso de instalación

1. **Clona o descarga este proyecto** y ubícate en su carpeta:
   ```bash
   cd visualizer_proyecto
   ```

2. **(Recomendado) Crea un entorno virtual:**
   ```bash
   python -m venv venv
   ```
   Actívalo:
   - Windows (PowerShell): `venv\Scripts\Activate.ps1`
   - Windows (cmd): `venv\Scripts\activate.bat`
   - macOS/Linux: `source venv/bin/activate`

3. **Instala las dependencias:**
   ```bash
   pip install opencv-python numpy
   ```

## Cómo ejecutar el programa

1. Ejecuta el script principal:
   ```bash
   python codigo_semana2.py
   ```

2. El programa te pedirá dos rutas de imagen, en este orden:
   1. **Imagen de un CÍRCULO** → ingresa la ruta, por ejemplo `circulo.jpg`.
   2. **Imagen de un CUADRADO** → ingresa la ruta, por ejemplo `cuadrado.png`.

   Puedes escribir la ruta relativa (si el archivo está en la misma carpeta) o la ruta absoluta. Las comillas alrededor de la ruta se aceptan y se eliminan automáticamente.

3. Tras calibrar, el programa imprime la circularidad detectada de cada referencia y **abre la cámara** automáticamente.

4. Muestra frente a la cámara una figura oscura sobre fondo claro (por ejemplo, una figura dibujada con marcador negro sobre papel blanco). El programa dibujará:
   - Un rectángulo verde alrededor del contorno detectado.
   - El valor de circularidad calculado.
   - La clasificación (`Circulo`, `Cuadrado` o `REVISION` si el resultado es ambiguo).

5. Presiona **Q** con la ventana de la cámara activa para cerrar el programa.

## Recomendaciones para mejores resultados

- Usa buena iluminación y evita sombras fuertes.
- La figura debe ser claramente más oscura que el fondo (fondo blanco/claro funciona mejor).
- La figura debe ocupar una parte considerable del cuadro de la cámara.
- Si la clasificación falla o siempre da `REVISION`, prueba ajustando el valor `THRESH` en el código (línea 10 de `codigo_semana2.py`) según la iluminación de tu entorno.

## Estructura del proyecto

```
visualizer_proyecto/
├── codigo_semana2.py   # Script principal (calibración + clasificación en vivo)
├── circulo.jpg         # Imagen de referencia de ejemplo (círculo)
├── cuadrado.png         # Imagen de referencia de ejemplo (cuadrado)
└── README.md           # Este archivo
```

## Solución de problemas

- **"No se pudo abrir la cámara"**: verifica que ninguna otra aplicación esté usando la cámara y que el índice `0` corresponda a tu cámara (en `cv2.VideoCapture(0)`).
- **"No pude detectar una figura clara en la imagen"**: usa una imagen con mejor contraste entre la figura y el fondo, o ajusta `THRESH`.
- **"No existe el archivo"**: revisa que la ruta ingresada sea correcta y que el archivo exista en esa ubicación.
