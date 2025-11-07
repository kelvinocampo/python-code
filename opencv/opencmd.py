import cv2
import mediapipe as mp
import subprocess
import time
import os
import psutil
import webbrowser

# --- 1. Inicialización de Modelos y Utilerías ---

# A) Inicializar Haar Cascade para Caras
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
if face_cascade.empty():
    print("ERROR: No se pudo cargar el archivo XML de Haar Cascade.")

# B) Inicializar MediaPipe para Manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Variables de control
ultimo_comando_tiempo = time.time()
PAUSA_COMANDO = 2  # Segundos de pausa después de ejecutar un comando
chrome_abierto = False  # Estado de Chrome

# --- 2. Funciones de Lógica ---

chrome_proceso = None
chrome_pid = None
chrome_controller = None  # Controlador del navegador

# Rutas posibles de Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"


def es_punio(hand_landmarks):
    """Verifica si el dedo índice está doblado (gesto de puño)."""
    punta_indice_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    base_indice_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
    return punta_indice_y > base_indice_y + 0.05


def detectar_dedos_levantados(hand_landmarks, handedness):
    """
    Detecta qué dedos están levantados en la mano derecha.
    Retorna un diccionario con el estado de cada dedo.
    """
    dedos = {
        "pulgar": False,
        "indice": False,
        "medio": False,
        "anular": False,
        "menique": False
    }
    
    # Obtener si es mano derecha o izquierda
    es_mano_derecha = handedness.classification[0].label == "Right"
    
    if not es_mano_derecha:
        return dedos
    
    # PULGAR (lógica diferente porque se mueve horizontalmente)
    punta_pulgar_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
    base_pulgar_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    
    if punta_pulgar_x < base_pulgar_x - 0.05:
        dedos["pulgar"] = True
    
    # ÍNDICE
    punta_indice_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    base_indice_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    if punta_indice_y < base_indice_y - 0.05:
        dedos["indice"] = True
    
    # MEDIO
    punta_medio_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    base_medio_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
    if punta_medio_y < base_medio_y - 0.05:
        dedos["medio"] = True
    
    # ANULAR
    punta_anular_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
    base_anular_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y
    if punta_anular_y < base_anular_y - 0.05:
        dedos["anular"] = True
    
    # MEÑIQUE
    punta_menique_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
    base_menique_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y
    if punta_menique_y < base_menique_y - 0.05:
        dedos["menique"] = True
    
    return dedos


def abrir_url_en_chrome(url):
    """Abre una URL en el Chrome controlado."""
    global chrome_abierto, chrome_controller
    
    if not chrome_abierto:
        print("⚠️ Chrome no está abierto. Abre Chrome primero con el puño izquierdo.")
        return
    
    try:
        # Usar el controlador del navegador registrado
        if chrome_controller:
            chrome_controller.open(url, new=2)  # new=2 abre en nueva pestaña
            print(f"✅ Abriendo URL en Chrome controlado: {url}")
        else:
            print("❌ No hay controlador de Chrome disponible")
    except Exception as e:
        print(f"❌ Error al abrir URL: {e}")


def accion_pulgar_derecho():
    """Abre YouTube en el Chrome abierto."""
    print("👍 PULGAR DERECHO: Abriendo YouTube")
    abrir_url_en_chrome("https://www.youtube.com")


def accion_indice_derecho():
    """Abre Gmail en el Chrome abierto."""
    print("☝️ ÍNDICE DERECHO: Abriendo Gmail")
    abrir_url_en_chrome("https://mail.google.com")


def accion_medio_derecho():
    """Abre Facebook en el Chrome abierto."""
    print("🖕 MEDIO DERECHO: Abriendo Facebook")
    abrir_url_en_chrome("https://www.facebook.com")


def accion_anular_derecho():
    """Abre Twitter/X en el Chrome abierto."""
    print("💍 ANULAR DERECHO: Abriendo Twitter")
    abrir_url_en_chrome("https://twitter.com")


def accion_menique_derecho():
    """Abre Wikipedia en el Chrome abierto."""
    print("🤙 MEÑIQUE DERECHO: Abriendo Wikipedia")
    abrir_url_en_chrome("https://www.wikipedia.org")


def abrir_chrome_incognito():
    """Abre Google Chrome en modo incógnito con perfil temporal."""
    global chrome_proceso, chrome_abierto, chrome_pid, chrome_controller

    if chrome_abierto:
        print("⚠️ Chrome ya está abierto.")
        return

    try:
        # Crear un perfil temporal para esta ventana específica
        temp_profile = os.path.join(os.getenv('TEMP'), 'chrome_gesture_profile')
        
        # Registrar Chrome con un nombre específico
        chrome_controller = webbrowser.get(f'"{chrome_path}" --incognito --user-data-dir="{temp_profile}" --no-first-run --no-default-browser-check %s')
        
        # Abrir la primera ventana
        chrome_controller.open("https://www.google.com", new=1)  # new=1 abre en nueva ventana
        
        chrome_abierto = True
        print(f"✅ Chrome abierto en modo incógnito con controlador.")
        
        # Esperar un momento para que Chrome inicie
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Error al abrir Chrome: {e}")
        chrome_abierto = False
        chrome_controller = None


def cerrar_chrome():
    """Cierra Chrome usando taskkill para el perfil específico."""
    global chrome_proceso, chrome_abierto, chrome_pid, chrome_controller
    
    if not chrome_abierto:
        print("⚠️ Chrome no está abierto.")
        return

    try:
        # Buscar y cerrar procesos de Chrome con nuestro perfil temporal
        temp_profile = os.path.join(os.getenv('TEMP'), 'chrome_gesture_profile')
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] == 'chrome.exe':
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                    if 'chrome_gesture_profile' in cmdline:
                        proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Esperar a que terminen los procesos
        time.sleep(1)
        
        chrome_abierto = False
        chrome_proceso = None
        chrome_pid = None
        chrome_controller = None
        print("🛑 Chrome cerrado completamente.")
        
    except Exception as e:
        print(f"❌ Error al cerrar Chrome: {e}")


# --- 3. Bucle Principal de Video ---

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: No se pudo abrir la cámara.")
    exit()

print(
    f"Iniciando detección. Presiona 'q' para salir. Pausa entre comandos: {PAUSA_COMANDO}s"
)
print("\n--- CONTROLES ---")
print("MANO IZQUIERDA:")
print("  - Puño: Abrir Chrome")
print("  - Mano abierta: Cerrar Chrome")
print("\nMANO DERECHA (cuando Chrome esté abierto):")
print("  - Pulgar: YouTube")
print("  - Índice: Gmail")
print("  - Medio: Facebook")
print("  - Anular: Twitter")
print("  - Meñique: Wikipedia\n")

gesto_actual = None
frame_count = 0
ESTABILIDAD_FRAMES = 5  # Número de frames consecutivos para confirmar gesto

# Variables para controlar dedos derechos
dedos_anteriores = {
    "pulgar": False,
    "indice": False,
    "medio": False,
    "anular": False,
    "menique": False
}
ultimo_comando_dedo = {
    "pulgar": 0,
    "indice": 0,
    "medio": 0,
    "anular": 0,
    "menique": 0
}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # --- A. Procesamiento de CARAS (Haar Cascades) ---
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    caras = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )
    for x, y, w, h in caras:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # --- B. Procesamiento de MANOS (MediaPipe) ---
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    gesto_detectado = None
    dedos_actuales = None
    
    # Comprobación de detección
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(
            results.multi_hand_landmarks, results.multi_handedness
        ):
            # Dibujar los puntos y conexiones de la mano
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
            )

            mano_etiqueta = handedness.classification[0].label

            # --- MANO IZQUIERDA: Control de Chrome ---
            if mano_etiqueta == "Left":
                if es_punio(hand_landmarks):
                    gesto_detectado = "PUNIO"
                    cv2.putText(
                        frame,
                        "PUÑO IZQUIERDO: ABRIR CHROME",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2,
                        cv2.LINE_AA,
                    )
                else:
                    gesto_detectado = "ABIERTA"
                    cv2.putText(
                        frame,
                        "MANO IZQUIERDA: CERRAR CHROME",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )
            
            # --- MANO DERECHA: Detección de dedos individuales ---
            elif mano_etiqueta == "Right":
                dedos_actuales = detectar_dedos_levantados(hand_landmarks, handedness)
                
                # Mostrar estado de dedos en pantalla
                y_pos = 200
                nombres_dedos = {
                    "pulgar": "Pulgar (YouTube)",
                    "indice": "Indice (Gmail)",
                    "medio": "Medio (Facebook)",
                    "anular": "Anular (Twitter)",
                    "menique": "Meñique (Wikipedia)"
                }
                
                for dedo, levantado in dedos_actuales.items():
                    color = (0, 255, 0) if levantado else (100, 100, 100)
                    estado = "✓" if levantado else "✗"
                    cv2.putText(
                        frame,
                        f"{estado} {nombres_dedos[dedo]}",
                        (50, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2,
                        cv2.LINE_AA,
                    )
                    y_pos += 30

    # --- Ejecutar comandos MANO IZQUIERDA con estabilidad ---
    tiempo_actual = time.time()
    puede_ejecutar = (tiempo_actual - ultimo_comando_tiempo) >= PAUSA_COMANDO

    # Contar frames consecutivos del mismo gesto
    if gesto_detectado == gesto_actual:
        frame_count += 1
    else:
        gesto_actual = gesto_detectado
        frame_count = 1

    # Ejecutar solo si el gesto es estable y ha pasado el tiempo de pausa
    if frame_count >= ESTABILIDAD_FRAMES and puede_ejecutar:
        if gesto_actual == "PUNIO" and not chrome_abierto:
            abrir_chrome_incognito()
            ultimo_comando_tiempo = tiempo_actual
            frame_count = 0
        elif gesto_actual == "ABIERTA" and chrome_abierto:
            cerrar_chrome()
            ultimo_comando_tiempo = tiempo_actual
            frame_count = 0

    # --- Ejecutar acciones MANO DERECHA (dedos individuales) ---
    if dedos_actuales:
        for dedo, levantado in dedos_actuales.items():
            # Detectar cambio de estado (de abajo a arriba)
            if levantado and not dedos_anteriores[dedo]:
                # Verificar pausa entre comandos del mismo dedo
                if (tiempo_actual - ultimo_comando_dedo[dedo]) >= PAUSA_COMANDO:
                    # Ejecutar acción según el dedo
                    if dedo == "pulgar":
                        accion_pulgar_derecho()
                    elif dedo == "indice":
                        accion_indice_derecho()
                    elif dedo == "medio":
                        accion_medio_derecho()
                    elif dedo == "anular":
                        accion_anular_derecho()
                    elif dedo == "menique":
                        accion_menique_derecho()
                    
                    ultimo_comando_dedo[dedo] = tiempo_actual
        
        # Actualizar estado anterior
        dedos_anteriores = dedos_actuales.copy()

    # --- Mostrar el Frame y Estado ---
    if tiempo_actual - ultimo_comando_tiempo < PAUSA_COMANDO:
        tiempo_restante = int(PAUSA_COMANDO - (tiempo_actual - ultimo_comando_tiempo))
        cv2.putText(
            frame,
            f"PAUSA: {tiempo_restante}s",
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

    # Mostrar estado de Chrome
    estado_chrome = "ABIERTO ✓" if chrome_abierto else "CERRADO ✗"
    color_estado = (0, 255, 0) if chrome_abierto else (0, 0, 255)
    cv2.putText(
        frame,
        f"Chrome: {estado_chrome}",
        (50, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color_estado,
        2,
        cv2.LINE_AA,
    )

    cv2.imshow("Deteccion y Control Gestual", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# --- 4. Liberar Recursos ---
cerrar_chrome()
cap.release()
cv2.destroyAllWindows()