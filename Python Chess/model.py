import keras
from keras import layers, activations

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

#model = neural_net()
#model.save("selftrain_model")





    
    


