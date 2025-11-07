# Plataforma de Monitoramento Ambiental para pátios Mottu com Node-RED

Este projeto implementa uma solução IoT para monitoramento temperamental em tempo real nos pátios da Mottu, utilizando sensores conectados a dispositivos ESP32/Arduino, com comunicação via MQTT e visualização em um dashboard Node-RED. A plataforma oferece alertas visuais e sonoros para condições críticas, gráficos históricos e indicadores LED virtuais.

O propósito deste projeto é fornecer uma maneira de rastrear e monitorar mudanças ambientais nos pátios Mottu, assim auxiliando-os a saber a condição das motos e o pátio que se encontram.


INTEGRANTES:

Eduardo do Nascimento Barriviera - RM555309

Thiago Lima de Freitas - RM556795

Bruno centurion Fernandes - RM556531

---

## 📸 Visão Geral


- Indicadores de temperatura, umidade e chuva nos pátios
- Alertas visuais (LEDs virtuais) e sonoros em tempo real
- Gráficos de histórico por sensor
- Dashboard responsivo e acessível

---

## ⚙️ Arquitetura da Solução

```plaintext
[Dispositivos IoT (ESP32/Arduino)]
          |
       MQTT (HiveMQ)
          |
      [Node-RED Gateway]
          |
     [Dashboard UI - Node-RED]
```

- Cada dispositivo coleta dados (temperatura, umidade, chuva)
- Os dados são publicados nos tópicos MQTT:
  - `iotfrontier/temperature`
  - `iotfrontier/humidity`
  - `iotfrontier/rain`
- O Node-RED se conecta ao broker MQTT, processa os dados, verifica condições de alerta e os exibe no dashboard.

---

## 🚀 Como Executar o Projeto

### 1. Requisitos

- Node.js instalado
- Node-RED instalado globalmente (`npm install -g node-red`)
- Navegador web (recomendado: Chrome ou Firefox)
- Conexão com broker MQTT (utiliza-se o broker público HiveMQ)

### 2. Instalar e Iniciar o Node-RED

```bash
node-red
```

Abra o navegador e acesse: [http://localhost:1880](http://localhost:1880)

### 3. Importar o Fluxo

- Clique no menu (☰) > "Import"
- Cole o conteúdo do fluxo JSON (ver seção abaixo)
- Clique em "Deploy"

### 4. Acessar o Dashboard

Acesse [http://localhost:1880/ui](http://localhost:1880/ui)

### 5. Testes

- Use um simulador de publicação MQTT (ex: MQTT Explorer ou MQTTBox) ou dispositivos reais
- Ou mude os valores de temperatura, umidade e chuva diretamente pelo potenciometro e dht do através do Wokw.
- Publique valores nos tópicos:
  - `iotfrontier/temperature` com valores > 30°C para acionar alerta
  - `iotfrontier/humidity` com valores > 70%
  - `iotfrontier/rain` com valores < 1500 (indicando chuva)

---

## 🔁 Fluxo Node-RED Explicado

### Entradas MQTT

- Três nós MQTT (`iotfrontier/temperature`, `iotfrontier/humidity`, `iotfrontier/rain`)
- Recebem dados dos sensores e encaminham para:
  - Gráficos (`ui_chart`)
  - Medidores (`ui_gauge`)
  - Função `Verifica Alertas`

### Função `Verifica Alertas`

```js
const val = parseFloat(msg.payload);
const topic = msg.topic;

let alert = {};

if (topic.includes("temperature") && val > 30) {
    alert.sound = true;
    alert.led_temp = true;
} else if (topic.includes("temperature")) {
    alert.led_temp = false;
}

if (topic.includes("humidity") && val > 70) {
    alert.led_humid = true;
} else if (topic.includes("humidity")) {
    alert.led_humid = false;
}

if (topic.includes("rain") && val < 1500) {
    alert.sound = true;
    alert.led_rain = true;
} else if (topic.includes("rain")) {
    alert.led_rain = false;
}

return { payload: alert };
```

### Saídas

- `ui_template (LEDs)`: exibe três LEDs virtuais (vermelho, azul, verde)
- `ui_template (Som de Alerta)`: toca som se `alert.sound` for verdadeiro

---

## 🧪 Testando com Simulador MQTT

```bash
# Exemplo usando MQTT CLI
mqtt pub -t iotfrontier/temperature -h broker.hivemq.com -m "31"
mqtt pub -t iotfrontier/humidity -h broker.hivemq.com -m "75"
mqtt pub -t iotfrontier/rain -h broker.hivemq.com -m "1400"
```

---

## 📁 Código-Fonte

- O fluxo principal está no arquivo `node-red-flow.json`
- O código dos dispositivos IoT se encontra no arquivo sketch.ino
- Todos os recursos visuais estão embutidos nos nós `ui_template`
- O projeto não depende de bibliotecas externas no lado do servidor

---

## 👥 Acesso Externo ao Dashboard

Por padrão, o Node-RED roda localmente. Para permitir o acesso externo:

1. Verifique seu IP local (ex: `192.168.1.10`)
2. Compartilhe o link `http://192.168.1.10:1880/ui`
3. Certifique-se de que:
   - O firewall libera a porta 1880
   - Os dispositivos estão na mesma rede

> Para acesso remoto via internet, considere usar **Ngrok**, **port forwarding** ou hospedar em um servidor cloud.

-------------------------------------------------------------------------------------------

# Parte 2: Visão computacional.

### Esta parte do projeto projeto utiliza **visão computacional** com **YOLOv5** e **OpenCV** para detectar motos em imagens e vídeos. O objetivo é identificar motos e status: **pronta para uso**, **em revisão**, **reservada**.
---
## 🔍 O que o código faz?
- Carrega um modelo YOLOv5 pré-treinado (yolov5s) para detectar objetos em tempo real.
- Abre um vídeo e processa frame a frame.
- Detecta motos (motorcycle) em cada frame.
- Desenha um retângulo verde em volta das motos detectadas e escreve o status da moto.
- Exibe o vídeo com as anotações.
---

## 🚀 Tecnologias Utilizadas

| Tecnologia | Descrição |
|------------|-----------|
| **Python 3** | Linguagem de programação usada no projeto. |
| **OpenCV** (`cv2`) | Biblioteca para manipulação de imagens e vídeos em tempo real. |
| **PyTorch** (`torch`) | Framework de machine learning usado para carregar o modelo YOLOv5. |
| **YOLOv5** | Modelo pré-treinado de detecção de objetos em tempo real. |
| **Ultralytics Hub** | Permite baixar modelos YOLOv5 diretamente via PyTorch Hub. |

---
O projeto conta com **3 scripts principais**:
| Arquivo | Tipo de entrada | Finalidade |
|--------|------------------|------------|
| `detectar_motos_simples.py` | 🎥 Vídeo | Detecta motos e marca como “pronta” com retângulo verde |
| `detectar_motos_2.py` | 🎥 Vídeo | Detecta motos e marca como "em revisão" com retângulos amarelos |
| `detectar_imagens.py` | 🖼️ Imagem | Detecta motos em uma imagem estática e amarca como "reservada" com retângulos azuis |

Cada um pode ser usado separadamente dependendo da sua fonte de entrada e objetivo.

---

## 📦 Requisitos

Antes de executar o projeto, você precisa ter:

- Python 3.7 ou superior instalado
- Pip atualizado

---

## 📥 Instalação

### 1. **Clone o repositório (ou salve o arquivo `.py`):**

```bash
git clone https://github.com/edu1805/CP05-IoT.git
cd seu-repositorio
```
### 2. **Instale as dependências:**

```bash
pip install torch torchvision opencv-python
```
```bash
pip install requests
```
```bash
pip install ultralytics
```
---

## 📹 Como usar

**Execute o script**
```bash
python detectar_motos_simples.py
```
para ver motos detectadas como "pronta";

**Execute o script**
```bash
python detectar_motos_2.py
```
para ver motos detectadas como "em revisão";

**Execute o script**
```bash
python detectar_imagens.py
```
para ver motos detectadas em uma imagem como "reservado".

> **🔴 Para encerrar o vídeo a qualquer momento, pressione a tecla Q.**

Arquivos referentes a parte de Visão Computacional que não afetam a parte de IoT de nenhuma maneira:

detectar_imagens.py;

detectar_motos_2.py;

detectar_motos_simples.py;

patio.mp4;

patio2.mp4;

patioimg.jpg;

yolov5s.pt.
