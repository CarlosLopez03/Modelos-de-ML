# -*- coding: utf-8 -*-
"""MarioIA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CG0ZoibAjM5Rnn697HUsxEUrlBw460P9

1. Configuración de Mario
"""

# Instalación de Mario y emulador
!pip install gym_super_mario_bros==7.3.0 nes_py

# Importación del juego
import gym_super_mario_bros
#Importación del Joypad
from nes_py.wrappers import JoypadSpace
#Importación de controles simplificados
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

# Commented out IPython magic to ensure Python compatibility.
import gym
from IPython import display
# Importación de Matplotlib para mostrar el impacto de los frames
import matplotlib.pyplot as plt
# %matplotlib inline
# Configuración del juego
env = gym_super_mario_bros.make('SuperMarioBros-v0')
env = JoypadSpace(env, SIMPLE_MOVEMENT)

# Crear una bandera - Para reiniciar o no
done = True
img = plt.imshow(env.render(mode='rgb_array'))
# Bucle a través de cada fotograma en el juego
for step in range(100000):
  # Empezar el juego para comenzar con: 
  if done:
    #Empezar juego
    env.reset()
  # Tomar acciones aleatorias
  action = env.action_space.sample()
  state, reward, done, info = env.step(action)
  # Mostrar el juego
  img.set_data(env.render(mode='rgb_array'))
  display.display(plt.gcf())
  display.clear_output(wait=True)
  #env.render('rgb_array')
# Cerrar juego
env.close()

"""2. Procesamiento del entorno"""

# Instalación pytorch
#!pip3 install torch torchvision torchaudio

# Instalación librerias de Ml
#!pip install stable-baselines3[extra]

# Importación de GraySacaling Wrapper
from gym.wrappers import GrayScaleObservation
# Importación Vectorization Wrappers
from stable_baselines3.common.vec_env import VecFrameStack, DummyVecEnv

# 1. Creación de la base de entornos
env = gym_super_mario_bros.make('SuperMarioBros-v0')
# 2. Simplificando los controles
env = JoypadSpace(env, SIMPLE_MOVEMENT)
# 3. Grayscale
env = GrayScaleObservation(env, keep_dim=True)
# 4. Envolver dentro del entorno ficticio
env = DummyVecEnv([lambda: env])
# 5. Apilar los frames
env = VecFrameStack(env, 4, channels_order='last')

state = env.reset()
state.shape
state, reward, done, info = env.step([env.action_space.sample()])

# Usando Matplotlib para mostrar los frame del juego
plt.figure(figsize=(12,8))
for idx in range(state.shape[3]):
  plt.subplot(1,4,idx+1)
  plt.imshow(state[0][:,:,idx])
plt.show()

"""3. Entrenamiento"""

# Importar OS para la gestión de la ruta de archivo
import os
# Importar PPO para ALgos
from stable_baselines3 import PPO
# Importar Base Callback para guardar los modelos
from stable_baselines3.common.callbacks import BaseCallback

# Función para guardar el modelo
# class TrainAndLoggingCallback(BaseCallback):

#     def __init__(self, check_freq, save_path, verbose=1):
#         super(TrainAndLoggingCallback, self).__init__(verbose)
#         self.check_freq = check_freq
#         self.save_path = save_path

#     def _init_callback(self):
#         if self.save_path is not None:
#             os.makedirs(self.save_path, exist_ok=True)

#     def _on_step(self):
#         if self.n_calls % self.check_freq == 0:
#             model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls))
#             self.model.save(model_path)

#         return True

# Configuración de directorios
# CHECKPOINT_DIR = './train/'
LOG_DIR = './logs/'

# Configuración del guardado del modelo
#callback = TrainAndLogginCallback(check_freq=10000, save_path=CHECKPOINT_DIR)

# Inicialización del modelo
model = PPO('CnnPolicy', env, verbose=1, tensorboard_log=LOG_DIR, learning_rate=0.000001, n_steps=512)

# Entrena el modelo AI, aquí es donde comienza el modelo AI a aprender
model.learn(total_timesteps=4096)

# Guardar modelo
model.save("ppo_cartpole")

"""4. Prueba"""

# Cargar el modelo
model = PPO.load("ppo_cartpole")

# Comienza el juego
state = env.reset()
img = plt.imshow(env.render(mode='rgb_array'))
# Bucle del juego
while True:
  img.set_data(env.render(mode='rgb_array'))
  display.display(plt.gcf())
  display.clear_output(wait=True)
  action, _state = model.predict(state)
  state, reward, done, info = env.step(action)

