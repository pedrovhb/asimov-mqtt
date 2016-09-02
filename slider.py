# -*- coding: utf-8 -*-
import pyglet
from pyglet.window import mouse
import math


class Slider:

    def __init__(self, x, y, valor_minimo, valor_maximo, valor_inicial, nome=''):

        assert valor_minimo < valor_maximo, 'Slider: Valor mínimo maior que valor máximo'
        assert valor_inicial <= valor_maximo, 'Slider: Valor inicial inválido, menor do que o valor mínimo'
        assert valor_inicial >= valor_minimo, 'Slider: Valor inicial inválido, menor do que o valor máximo'

        self.x = x
        self.y = y

        self.valor_min = valor_minimo
        self.valor_max = valor_maximo
        self.valor = valor_inicial

        self.slider_movendo = False

        self.imagem_barra = pyglet.image.load('resources/bar.png')

        self.imagem_barra.anchor_x = self.imagem_barra.width / 2
        self.imagem_barra.anchor_y = self.imagem_barra.height / 2

        self.sprite_barra = pyglet.sprite.Sprite(self.imagem_barra, x=self.x, y=self.y)
        self.sprite_slider = pyglet.sprite.Sprite(self.imagem_barra, x=self.x, y=self.y)

        self.sprite_slider.rotation = 90
        self.sprite_slider.scale = 0.3

        self.nome = nome
        self.label_nome = pyglet.text.Label(nome,
                                            font_name='Times New Roman',
                                            font_size=20,
                                            x=x, y=y - self.sprite_barra.height/2 - self.sprite_barra.height/10,
                                            anchor_x='center', anchor_y='center', color=(28, 28, 28, 255))

    def slider_draw(self):
        self.sprite_barra.draw()
        self.sprite_slider.y = self.y - self.sprite_barra.height/2 \
                               + float(self.valor) / (self.valor_max - self.valor_min) * self.sprite_barra.height
        self.sprite_slider.draw()
        self.label_nome.draw()

    def slider_calcular_parametros(self, x, y):
        self.valor = float(y - self.y + self.sprite_barra.height/2)/self.sprite_barra.height \
                           * float(self.valor_max - self.valor_min) + self.valor_min
        if self.valor < self.valor_min:
            self.valor = self.valor_min
        elif self.valor > self.valor_max:
            self.valor = self.valor_max

    def slider_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # Obter posição do joystick
        if buttons & mouse.LEFT and self.slider_movendo:
            self.slider_calcular_parametros(x, y)

    def slider_mouse_press(self, x, y, button, modifiers):
        # Comparação com altura porque o atributo não considera rotação, mas considera scale
        if math.fabs(self.x - x) < self.sprite_slider.height and math.fabs(self.y - y) < self.sprite_barra.height:
            self.slider_movendo = True
            self.slider_calcular_parametros(x, y)

    def slider_mouse_release(self, x, y, button, modifiers):
        self.slider_movendo = False

