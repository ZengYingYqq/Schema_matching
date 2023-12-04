from tensorflow import keras
from tensorflow.keras import layers
import data

train = data.train
print(train.shape)
labels = data.train_label
test = data.data

model = keras.Sequential([
    layers.Input(shape=(768,)),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(train, labels, epochs=20, steps_per_epoch=len(train))

model.save('model.h5')

# model = keras.models.load_model('model.h5')

predictions = model.predict(test)

for i in range(0, predictions.size):
    print(data.result[i] + str(predictions[i]))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
