import cv2
import mediapipe as mp

# Initialisation MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils # Pour dessiner les lignes
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Préparation de l'image
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False # Optimisation mémoire
    
    # 2. Détection
    results = pose.process(image)
    
    # 3. Dessin et Logique
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # Repasser en BGR pour OpenCV

    if results.pose_landmarks:
        # Dessiner le squelette sur l'image
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )

        # Extraction des points pour ton futur modèle
        landmarks = results.pose_landmarks.landmark
        
        # EXEMPLE : Détection simplifiée de "Chute" (Logique géométrique)
        # Si la tête (0) est plus basse que les hanches (24)
        head_y = landmarks[mp_pose.PoseLandmark.NOSE].y
        hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y
        
        if head_y > hip_y:
            cv2.putText(image, "ALERTE: CHUTE POSSIBLE", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Affichage
    cv2.imshow('SafeHome Live Detection', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()