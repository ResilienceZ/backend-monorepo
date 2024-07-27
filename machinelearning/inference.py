import tensorflow as tf

def predict(val):
    model = tf.keras.models.load_model('./machinelearning/model.h5')
    return model.predict([val])