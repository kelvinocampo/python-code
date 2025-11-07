import cv2

# Cargar el clasificador pre-entrenado para caras frontales
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detectar_caras(frame):
    # Convertir a escala de grises, ya que Haar funciona mejor así
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar caras
    # (Parámetros ajustables: scaleFactor y minNeighbors)
    caras = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Dibujar un rectángulo alrededor de cada cara
    for (x, y, w, h) in caras:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
    return frame

# --- Ejemplo de uso con cámara ---
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    frame_con_caras = detectar_caras(frame)
    
    cv2.imshow('Deteccion de Caras', frame_con_caras)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()