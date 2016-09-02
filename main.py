# -*- coding: utf-8 -*-

import pyglet
from pyglet.window import key
import paho.mqtt.client as mqtt
from joystick import Joystick
from slider import Slider
from datetime import datetime, timedelta

window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Aqui criamos o dicionário onde serão guardados os valores de controle do Asimov.
asimov = dict()
asimov['dir'] = 0
asimov['vel'] = 0
asimov['farois'] = 0
asimov['cooler'] = 0
asimov['cmd'] = 'v0d0f0c0'


#########################################
# Paho MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Na conexão, nos inscrevemos no tópico 'ASIMOV_ANSWER', por onde virão as mensagens do Asimov.
    client.subscribe("ASIMOV_ANSWER")


# Callback de quando recebemos uma mensagem, atualizando a estampa de tempo.
def on_message(client, userdata, msg):
    print(msg.topic+": "+str(msg.payload))
    global ultima_mensagem_recebida
    ultima_mensagem_recebida = datetime.now()

##########################################
# Pyglet


def update(dt, client):

    global conexao_ativa
    # Verificamos se o tempo entre agora e a última mensagem recebida excedeu o timeout determinado.
    if datetime.now() > ultima_mensagem_recebida + timeout:
        conexao_ativa = False
        conexao_ativa_display.text = 'OFFLINE'
        conexao_ativa_display.color = (255, 57, 49, 255)
    else:
        conexao_ativa = True
        conexao_ativa_display.text = 'ONLINE'
        conexao_ativa_display.color = (57, 255, 49, 255)

    # Aqui pegamos os valores dos elementos de controle e os utilizamos
    # para formar uma mensagem em formato que o Asimov entenda.
    asimov['vel'] = int(joystick.velocidade)
    asimov['dir'] = int(joystick.angulo)
    asimov['farois'] = int(slider_farois.valor)
    asimov['cooler'] = int(slider_cooler.valor)
    asimov['cmd'] = 'v' + str(asimov['vel']) + 'd' + str(asimov['dir']) + 'f' \
                    + str(asimov['farois']) + 'c' + str(asimov['cooler'])

    # Usamos o cliente MQTT para publicar o comando no canal em que o Asimov se inscreveu, ASIMOV_CMD
    client.publish('ASIMOV_CMD', asimov['cmd'])


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    joystick.joy_mouse_drag(x, y, dx, dy, buttons, modifiers)
    for slider in sliders:
        slider.slider_mouse_drag(x, y, dx, dy, buttons, modifiers)


@window.event
def on_mouse_release(x, y, button, modifiers):
    joystick.joy_mouse_release(x, y, button, modifiers)
    for slider in sliders:
        slider.slider_mouse_release(x, y, button, modifiers)


@window.event
def on_mouse_press(x, y, button, modifiers):
    joystick.joy_mouse_press(x, y, button, modifiers)
    for slider in sliders:
        slider.slider_mouse_press(x, y, button, modifiers)


@window.event
def on_draw():
    pyglet.gl.glClearColor(0.4, 0.4, 0.45, 1)
    window.clear()

    joystick.joy_draw()
    titulo_asimov.draw()
    conexao_ativa_display.draw()

    for slider in sliders:
        slider.slider_draw()

# Conexão do paho-mqtt configurado para acessar o broker na rede local
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.14.109", 1883, 60)
client.loop_start()

# Fazemos um sistema de timeout para identificar a desconexão do Asimov ou do cliente ao broker.
# Guardamos uma estampa de tempo que é atualizada a cada mensagem que recebemos do Asimov. Também definimos o
# timeout como sendo de 3 segundos. Quando fazemos update, o programa verifica se faz mais de três segundos que
# recebemos a última mensagem, e daí avisa o status da conexão. Configuramos o status inicial da última mensagem
# recebida com uma data mais antiga, para que o programa inicie como "offline" e mude para "online" se confirmar
# a conexão.
conexao_ativa = False
ultima_mensagem_recebida = datetime.now() - timedelta(days=100)
timeout = timedelta(seconds=3)

titulo_asimov = pyglet.text.Label('Asimov MQTT',
                                  font_name='Times New Roman',
                                  font_size=40, bold=True,
                                  x=window.width//2, y=window.height - window.height//6,
                                  anchor_x='center', anchor_y='center', color=(28, 28, 28, 255))

conexao_ativa_display = pyglet.text.Label('OFFLINE',
                                          font_name='Times New Roman',
                                          font_size=36,
                                          x=window.width//2, y=window.height - window.height//3,
                                          anchor_x='center', anchor_y='center', color=(255, 57, 49, 255))

# Instanciamos as classes de controle criadas.
joystick = Joystick(window.width/3, window.height/3)
slider_cooler = Slider(window.width - window.width/3, window.height/3, 0, 255, 200, 'Cooler')
slider_farois = Slider(window.width - window.width/3 + window.width/6, window.height/3, 0, 255, 0, u'Faróis')
sliders = [slider_cooler, slider_farois]

# Aqui, definimos update como a função a ser chamada a cada segundo.
# Passamos o cliente MQTT para que ele possa ser usado para publicar mensagens.
pyglet.clock.schedule_interval(update, 1, client)
pyglet.app.run()
