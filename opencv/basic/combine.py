import cv2
import mediapipe as mp
import numpy as np # Necesario para algunas operaciones internas de OpenCV

# --- 1. Inicialización de Modelos ---

# A) Inicializar Haar Cascade para Caras (Opencv nativo)
# Utilizamos la función cv2.data.haarcascades para obtener la ruta
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# B) Inicializar MediaPipe para Manos (Google)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# --- 2. Inicialización de la Cámara ---

cap = cv2.VideoCapture(0)

print("Iniciando detección. Presiona 'q' para salir...")

# --- 3. Bucle Principal de Procesamiento ---

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame de la cámara.")
        break
        
    # --- PROCESAMIENTO DE CARAS (OpenCV) ---
    
    # 1. Convertir a escala de grises para el detector de Haar
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 2. Detectar caras
    caras = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # 3. Dibujar rectángulos en las caras
    for (x, y, w, h) in caras:
        # Dibujar rectángulo azul para las caras (BGR: Azul)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)


    # --- PROCESAMIENTO DE MANOS (MediaPipe) ---

    # 1. Convertir a RGB (MediaPipe prefiere RGB)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 2. Procesar la imagen con el modelo de manos
    results = hands.process(image_rgb)
    
    # 3. Dibujar los resultados de las manos
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibuja los puntos y las conexiones verdes
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                # Estilo de puntos (verde)
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4)
            )

    # --- Mostrar el Frame ---
    cv2.imshow('Deteccion Unificada: Caras y Manos', frame)
    
    # Salir al presionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- 4. Liberar Recursos ---
cap.release()
cv2.destroyAllWindows()