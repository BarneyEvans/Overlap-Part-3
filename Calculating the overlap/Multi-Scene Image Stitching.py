import tensorflow as tf
from tensorflow.keras import layers, models

def create_shared_encoder(input_shape):
    """
    Create the shared encoder with 8 convolutional layers and 3 max-pooling layers.
    """
    inputs = tf.keras.Input(shape=input_shape)

    # Encoder Convolutional Layers with Batch Normalization
    x = inputs
    for filters in [64] * 4 + [128] * 4:
        x = layers.Conv2D(filters, (3, 3), activation='relu', padding='same')(x)
        x = layers.BatchNormalization()(x)

    # Encoder Max-Pooling Layers
    for _ in range(3):
        x = layers.MaxPooling2D((2, 2))(x)

    model = models.Model(inputs=inputs, outputs=x, name="shared_encoder")
    return model

def add_descriptor_decoder(encoder_model):
    """
    Add a descriptor decoder to the shared encoder for generating descriptors.
    """
    x = encoder_model.output

    # Convolutional layers specific to descriptor decoding
    x = layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    descriptors = layers.Conv2D(256, (1, 1), activation='relu')(x)  # Output descriptors

    # Upsample to match the input image size
    descriptors_upsampled = layers.UpSampling2D(size=(8, 8), interpolation='bicubic')(descriptors)

    # Model incorporating both the shared encoder and the descriptor decoder
    model = models.Model(inputs=encoder_model.input, outputs=descriptors_upsampled, name="descriptor_decoder")
    return model

def add_feature_point_decoder(encoder_model):
    """
    Add a fine-positioned feature point decoder to the shared encoder.
    """
    x = encoder_model.output

    # Upsampling and convolution to predict feature points
    x = layers.UpSampling2D(size=(8, 8), interpolation='bilinear')(x)
    feature_points = layers.Conv2D(1, (1, 1), activation='sigmoid', name="feature_points")(x)

    # Model incorporating both the shared encoder and the feature point decoder
    model = models.Model(inputs=encoder_model.input, outputs=feature_points, name="feature_point_decoder")
    return model

# Define the full model
input_shape = (256, 256, 3)  # Adjust based on your dataset
shared_encoder = create_shared_encoder(input_shape)

# Extend the shared encoder with both decoders
descriptor_model = add_descriptor_decoder(shared_encoder)
feature_point_model = add_feature_point_decoder(shared_encoder)

# Display model summaries
descriptor_model.summary()
feature_point_model.summary()

# Note: Custom training loops and loss functions will be needed to train this model.
