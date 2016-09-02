# -*- coding: utf-8 -*-
import pyglet
from pyglet.window import mouse
import math


class Joystick:

    def __init__(self, x, y, velocidade_maxima=255):
        # Pega posição, dimensões e dicionário asimov a ser modificado
        self.x = x
        self.y = y
        self.angulo = 0
        self.distancia = 0
        self.velocidade = 0
        self.velocidade_maxima = velocidade_maxima

        self.joyX = self.x
        self.joyY = self.y
        self.joy_movendo = False

        self.imagem_circulo = pyglet.image.load('resources/circle.png')

        self.imagem_circulo.anchor_x = self.imagem_circulo.width / 2
        self.imagem_circulo.anchor_y = self.imagem_circulo.height / 2

        self.sprite_imagem_circulo = pyglet.sprite.Sprite(self.imagem_circulo, x=self.x, y=self.y)
        self.sprite_circulo_dentro = pyglet.sprite.Sprite(self.imagem_circulo, x=self.x, y=self.y)

        self.sprite_imagem_circulo.scale = 1
        self.sprite_circulo_dentro.scale = 0.2

    def joy_draw(self):
        self.sprite_imagem_circulo.draw()
        self.sprite_circulo_dentro.set_position(self.joyX, self.joyY)
        self.sprite_circulo_dentro.draw()

    def joy_calcular_parametros(self, x, y):

        # Calcula-se o ângulo através de arcotg(y/x); aqui evitamos divisões por 0
        if x - self.x == 0:
            if self.y - y < 0:
                angulo_rad = 3*math.pi/2
            else:
                angulo_rad = math.pi/2
        else:
            # Obter Ângulo em relação ao centro do joystick
            angulo_rad = math.atan((float(y - self.y)) / (float(x - self.x)))

        self.angulo = angulo_rad*(180 / math.pi)*-1  # Transformar radianos em graus
        self.angulo -= 90  # Fixar o ângulo 0 como para cima
        # Ajuste de sinal
        if x - self.x > 0:
            self.angulo += 180

        # Calcular velocidade (distância entre centro do joystick e mouse), limitar ao raio
        self.distancia = math.sqrt(math.pow(self.x - x, 2) + math.pow(self.y - y, 2))
        raio = self.sprite_imagem_circulo.width/2

        # Limitar velocidade a velocidade_máxima
        self.velocidade = min(self.velocidade_maxima, (self.distancia/raio) * self.velocidade_maxima)

        # Limitar joystick ao raio do círculo maior
        if self.distancia > raio:
            # Ajustar sinal
            if self.x - x < 0:
                self.joyX = self.x + math.cos(angulo_rad) * raio
                self.joyY = self.y + math.sin(angulo_rad) * raio
            else:
                self.joyX = self.x - math.cos(angulo_rad) * raio
                self.joyY = self.y - math.sin(angulo_rad) * raio
        else:
            self.joyX = x
            self.joyY = y

    def joy_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # Obter posição do joystick
        if buttons & mouse.LEFT and self.joy_movendo:
            self.joy_calcular_parametros(x, y)

    def joy_mouse_release(self, x, y, button, modifiers):
        # Ao soltar o botão esquerdo do mouse, o joystick volta à sua posição inicial.
        if button == mouse.LEFT:
            self.joy_movendo = False
            self.joy_calcular_parametros(self.x, self.y)

    def joy_mouse_press(self, x, y, button, modifiers):
        # Ao clicar o mouse, verificar se o clique foi dentro da área do joystick. Se for, estamos o acionando
        if button == mouse.LEFT:
            # Se a distância até o centro do joystick for menor do que seu raio, temos um clique dentro
            if math.sqrt(math.pow(self.x - x, 2) + math.pow(self.y - y, 2)) < self.sprite_imagem_circulo.width/2:
                self.joy_movendo = True
                self.joy_calcular_parametros(x, y)















