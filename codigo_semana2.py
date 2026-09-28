import cv2
import numpy as np
import math
import os

# =========================
# CONFIG
# =========================
MIN_AREA = 50          # ignora contornos pequeños
THRESH = 100           # umbral fijo (ajustable)

# =========================
# UTILIDADES
# =========================
def circularity(area, perimeter):
    if perimeter == 0:
        return 0.0
    return 4 * math.pi * area / (perimeter * perimeter)

def preprocess_for_contours(img_bgr):
    """Convierte a binaria para encontrar contornos."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Asume figura oscura sobre fondo claro:
    _, binary = cv2.threshold(blur, THRESH, 255, cv2.THRESH_BINARY_INV)
    return binary

def biggest_contour(binary_img):
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    cnt = max(contours, key=cv2.contourArea)
    if cv2.contourArea(cnt) < MIN_AREA:
        return None
    return cnt

def contour_metrics(cnt):
    area = cv2.contourArea(cnt)
    perim = cv2.arcLength(cnt, True)
    circ = circularity(area, perim)
    return area, perim, circ

def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {path}")
    return img

def ask_image_path(prompt):
    print(prompt)
    path = input("Ruta del archivo (jpg/png): ").strip().strip('"')
    if not os.path.exists(path):
        raise FileNotFoundError(f"No existe el archivo: {path}")
    return path

def calibrate_reference(path, label):
    """
    Lee una imagen de referencia, encuentra el contorno principal
    y devuelve su circularidad como "patrón" simple.
    """
    img = load_image(path)
    binary = preprocess_for_contours(img)
    cnt = biggest_contour(binary)

    if cnt is None:
        raise ValueError(
            f"No pude detectar una figura clara en la imagen de {label}.\n"
            f"Tip: usa figura oscura en fondo claro y que ocupe buena parte de la imagen."
        )

    area, perim, circ = contour_metrics(cnt)
    print(f"✅ Referencia {label}: circularidad={circ:.3f}, area={area:.0f}")
    return circ

def decide_by_reference(circ_value, circ_circle_ref, circ_square_ref):
    """
    Si circularidad < 0.5 => NO clasifica (label vacío)
    """
    if circ_value < 0.5:
        return ("", None, None)

    d_circle = abs(circ_value - circ_circle_ref)
    d_square = abs(circ_value - circ_square_ref)

    # Zona de duda
    if abs(d_circle - d_square) < 0.05:
        return ("REVISION", d_circle, d_square)

    if d_circle < d_square:
        return ("Circulo", d_circle, d_square)
    else:
        return ("Cuadrado", d_circle, d_square)

# =========================
# PROGRAMA PRINCIPAL
# =========================
def main():
    print("=== Calibración de Formas (Circulo vs Cuadrado) ===")
    print("Usa imágenes con figura oscura sobre fondo claro (ej. papel blanco + marcador negro).")
    print("")

    # 1) Pedir imagen de círculo
    circle_path = ask_image_path("1) Ingrese una IMAGEN de un CIRCULO.")
    circ_circle_ref = calibrate_reference(circle_path, "Circulo")

    # 2) Pedir imagen de cuadrado
    square_path = ask_image_path("2) Ingrese una IMAGEN de un CUADRADO.")
    circ_square_ref = calibrate_reference(square_path, "Cuadrado")

    print("\n✅ Calibración lista. Abriendo cámara...")
    print("Mostrá un círculo o un cuadrado frente a la cámara.")
    print("Presioná Q para salir.\n")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara (verifica permisos o índice 0).")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        binary = preprocess_for_contours(frame)
        cnt = biggest_contour(binary)

        if cnt is not None:
            area, perim, circ_val = contour_metrics(cnt)

            label, d_circle, d_square = decide_by_reference(
                circ_val, circ_circle_ref, circ_square_ref
            )

            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Siempre mostrar circularidad (útil para depurar)
            cv2.putText(frame, f"circularidad={circ_val:.2f}", (15, 85),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)

            # Solo mostrar label y distancias si hay clasificación
            if label:
                cv2.putText(frame, label, (15, 45),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3)

                if d_circle is not None:
                    cv2.putText(frame, f"dist(C)={d_circle:.2f} dist(Q)={d_square:.2f}", (15, 115),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 50), 2)

        else:
            cv2.putText(frame, "Muestre una figura (oscura) sobre fondo claro", (15, 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)

        cv2.imshow("Clasificador", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Programa finalizado.")

if __name__ == "__main__":
    main()