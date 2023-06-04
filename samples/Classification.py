import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from PIL import Image

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

def training():
    # ニューラルネットワークの構築
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28), name="flatten_"),     #28x28配列を1次元配列にする(入力層)
        tf.keras.layers.Dense(128, activation="relu"),                      #ReLU関数を使用(中間層)
        tf.keras.layers.Dropout(0.2),                                       #直前のノードを無効にして過学習を防ぐ
        tf.keras.layers.Dense(10, activation="softmax")                     #出力層として10個のノードを持つ
    ], "classification_model")

    model.compile(optimizer="adam",
                loss="sparse_categorical_crossentropy",
                metrics=[tf.keras.metrics.sparse_categorical_accuracy])

    callbacks = [tf.keras.callbacks.EarlyStopping(patience=2, restore_best_weights=True)]

    model.fit(x_train, y_train, batch_size=128, epochs=20,
                        validation_split=0.2, callbacks=callbacks)

    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print(test_loss)
    print(test_acc)

    model.save("Datas/Models/mnist_classification_model.h5")

def Load_Model():
    model = tf.keras.models.load_model("./Datas/Models/mnist_classification_model.h5")

    for i in range(1, 10):    
        img = Image.open(f"./Datas/img/{i}.png").convert("L").resize((28, 28))
        img = np.array(img) / 255
        img = np.squeeze(img)
        img_expand = np.expand_dims(img, 0)
        predictions_single = model.predict(img_expand)
        print("----- predict -----")
        print(predictions_single[0].argmax())
        print("-------------------")

Load_Model()