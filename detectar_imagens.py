import cv2
import torch

# Carregar modelo YOLOv5 pré-treinado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Carregar imagem
img = cv2.imread('patioimg.jpg')  # Substitua pelo nome/caminho da sua imagem

# Realizar a detecção
results = model(img)

# Processar as detecções
for *box, conf, cls in results.xyxy[0]:
    x1, y1, x2, y2 = map(int, box)
    classe = int(cls)
    label = model.names[classe]

    if label == "motorcycle":
        # Azul em BGR
        cor = (255, 0, 0)

        # Desenhar retângulo
        cv2.rectangle(img, (x1, y1), (x2, y2), cor, 2)

        # Texto "reservado"
        texto = "reservado"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        text_size = cv2.getTextSize(texto, font, font_scale, thickness)[0]

        text_x = x1 + (x2 - x1) // 2 - text_size[0] // 2
        text_y = y1 - 15 if y1 - 15 > 10 else y1 + 15

        cv2.putText(img, texto, (text_x, text_y), font, font_scale, cor, thickness)

# Mostrar imagem com detecções
cv2.imshow('Detecção de Motos - Reservado (Azul)', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
