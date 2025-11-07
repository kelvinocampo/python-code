import cv2
import mediapipe as mp

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False, # Procesar video (False)
    max_num_hands=2,         # Detectar hasta 2 manos
    min_detection_confidence=0.5 # Confianza mínima
)
mp_drawing = mp.solutions.drawing_utils # Utilidad para dibujar los puntos

def detectar_manos(frame):
    # Convertir a RGB (MediaPipe prefiere RGB)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Procesar la imagen
    results = hands.process(image_rgb)
    
    # Dibujar los resultados
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Dibuja las líneas de conexión de la mano
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                # Opcional: Personalizar el estilo de los puntos
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4)
            )
            
    return frame

# --- Ejemplo de uso con cámara ---
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    frame_con_manos = detectar_manos(frame)
    
    cv2.imshow('Deteccion de Manos', frame_con_manos)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()