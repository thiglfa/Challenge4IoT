import cv2
import torch

# Carregar modelo YOLOv5 pré-treinado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Abrir vídeo
cap = cv2.VideoCapture('patio2.mp4')  # Substitua pelo caminho do seu vídeo

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detecção
    results = model(frame)

    for *box, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, box)
        classe = int(cls)
        label = model.names[classe]

        if label == "motorcycle":
            # Cor amarela
            cor = (0, 255, 255)

            # Desenhar retângulo
            cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)

            # Texto "em revisão" acima do retângulo
            texto = "em revisao"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2
            text_size = cv2.getTextSize(texto, font, font_scale, thickness)[0]

            # Posição do texto: centralizado acima do retângulo
            text_x = x1 + (x2 - x1) // 2 - text_size[0] // 2
            text_y = y1 - 15 if y1 - 15 > 10 else y1 + 15

            cv2.putText(frame, texto, (text_x, text_y), font, font_scale, cor, thickness)

    # Mostrar frame
    cv2.imshow('Detecção de Motos - Em Revisão', frame)

    # Sair com 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
