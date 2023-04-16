import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# ニューラルネットワークの構築
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28), name="flatten_"),     #28x28配列を1次元配列にする(入力層)
    tf.keras.layers.Dense(128, activation="relu"),                      #ReLU関数を使用(中間層)
    tf.keras.layers.Dropout(0.2),                                       #直前のノードを無効にして過学習を防ぐ
    tf.keras.layers.Dense(10, activation="softmax")                     #出力層として10個のノードを持つ
], "classification_model")

model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])