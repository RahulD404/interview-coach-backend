import cv2
import mediapipe as mp

# ✅ Proper initialization
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)


def extract_frames(video_path, max_frames=60, step=3):
    cap = cv2.VideoCapture(video_path)

    frames = []
    count = 0
    idx = 0

    while cap.isOpened() and count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        if idx % step == 0:   # 🔥 sample frames (important for DeepFace)
            frames.append(frame)
            count += 1

        idx += 1

    cap.release()
    return frames


def detect_landmarks(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        return result.multi_face_landmarks[0]
    return None