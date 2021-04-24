import keras
from keras import layers

def neural_net():
    
    model = keras.Sequential()

    model.add(layers.Conv2D(128, kernel_size = (2, 2), activation = 'relu',
                    input_shape = (8,8,6), padding = 'same'))
    model.add(layers.BatchNormalization())
    
    model.add(layers.Conv2D(128, kernel_size = (2, 2), activation = 'relu', padding = 'same'))
    model.add(layers.BatchNormalization())
    
    model.add(layers.Conv2D(64, kernel_size = (2, 2), activation = 'relu', padding = 'same'))
    model.add(layers.BatchNormalization())
    
    model.add(layers.Flatten())
    
    model.add(layers.Dense(64, activation = 'relu'))
    
    model.add(layers.Dense(1, activation = 'tanh'))
    
    opt = keras.optimizers.Adam(learning_rate=0.01)
    model.compile(loss = 'hinge',
              optimizer = opt,
              metrics=['accuracy'])
    
    return model






    
    


