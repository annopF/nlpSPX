
import tensorflow as tf
from tensorflow.python.client import device_lib
import torch

print("GPU device info:")

print("------------------------------------------------ PyTorch")
print("PyTorch GPU status: ",torch.cuda.is_available())
print("------------------------------------------------ Tensorflow")
print("Tensorflow version: ",tf.__version__)
print("Tensorflow GPU status: ", tf.test.is_built_with_cuda)
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')),"\n")

print("GPU name: ",tf.test.gpu_device_name())
print("end of info")
print("tset")
