
from tensorflow.keras.layers import Input, Dense, Flatten, Concatenate
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model

def build_model(num_features):
    # CNN branch
    cnn_base = MobileNetV2(weights=None, include_top=False, input_shape=(224,224,3))
    x = Flatten()(cnn_base.output)

    # Clinical branch
    clinical_input = Input(shape=(num_features,))
    c = Dense(32, activation='relu')(clinical_input)
    c = Dense(16, activation='relu')(c)

    # Fusion
    combined = Concatenate()([x, c])
    z = Dense(64, activation='relu')(combined)

    image_out = Dense(4, activation='softmax', name="image_class")(z)
    stage_out = Dense(6, activation='softmax', name="stage")(z)
    prog_out = Dense(4, activation='softmax', name="prognosis")(z)

    model = Model(inputs=[cnn_base.input, clinical_input],
                  outputs=[image_out, stage_out, prog_out])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics={'image_class': 'accuracy', 'stage': 'accuracy', 'prognosis': 'accuracy'}
    )
    return model
