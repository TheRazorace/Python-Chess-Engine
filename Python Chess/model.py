import keras
from keras import layers, activations, models

def neural_net():
    
    model = keras.Sequential()

    model.add(layers.Conv2D(128, kernel_size = (3, 3), 
                    input_shape = (8,8,6), padding = 'same'))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation(activations.relu))
    
    model.add(layers.Conv2D(128, kernel_size = (3, 3), padding = 'same'))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation(activations.relu))
    
    model.add(layers.Conv2D(64, kernel_size = (3, 3), padding = 'same'))
    model.add(layers.BatchNormalization())
    model.add(layers.Activation(activations.relu))
    
    model.add(layers.Flatten())
    
    model.add(layers.Dense(64, activation = 'relu'))
    
    model.add(layers.Dense(1, activation = 'tanh'))
    
    opt = keras.optimizers.SGD(learning_rate=0.01, momentum = 0.3)
    model.compile(loss = "mean_squared_error",
              optimizer = opt,
              metrics=['accuracy'])
    
    return model

def refined_model():
    
    chessboard_input = layers.Input(shape = (8,8,6))
    turn_input = layers.Input( shape = (1,))
    
    conv1 = layers.Conv2D(128, kernel_size = (3, 3), padding = 'same')(chessboard_input)
    bn1 = layers.BatchNormalization()(conv1)
    act1 = layers.Activation(activations.relu)(bn1)
    
    conv2 = layers.Conv2D(128, kernel_size = (3, 3), padding = 'same')(act1)
    bn2 = layers.BatchNormalization()(conv2)
    act2 = layers.Activation(activations.relu)(bn2)
    
    conv3 = layers.Conv2D(64, kernel_size = (3, 3), padding = 'same')(act2)
    bn3 = layers.BatchNormalization()(conv3)
    act3 = layers.Activation(activations.relu)(bn3)
    
    flatten = layers.Flatten()(act3)
    merge = layers.concatenate([flatten, turn_input])
    
    d1 = layers.Dense(64, activation = 'relu')(merge)
    out = layers.Dense(1, activation = 'tanh')(d1)
    
    model = models.Model(inputs = [chessboard_input, turn_input], outputs = out)
    opt = keras.optimizers.SGD(learning_rate=0.001, momentum = 0.3)
    model.compile(loss = "mean_squared_error",
              optimizer = opt,
              metrics=['accuracy'])
    
    return model

model = refined_model()
model.save("selftrain2_model")









    
    


