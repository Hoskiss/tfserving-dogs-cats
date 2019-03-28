import os
import shutil
import tensorflow as tf
(HEIGHT, WIDTH, CHANNELS) = (299, 299, 3)

def serving_input_receiver_fn():
    """Convert string encoded images (like base64 strings) into preprocessed tensors"""

    # https://stackoverflow.com/questions/44942729/tensorflowvalueerror-images-contains-no-shape
    def decode_and_resize(image_str_tensor):
        """Decodes a single image string, preprocesses/resizes it, and returns a reshaped uint8 tensor."""
        image_decoded = tf.cond(
            tf.image.is_jpeg(image_str_tensor),
            lambda: tf.image.decode_jpeg(
                image_str_tensor, channels=CHANNELS),
            lambda: tf.image.decode_png(
                image_str_tensor, channels=CHANNELS))
        #image = tf.image.decode_image(image_str_tensor, channels=CHANNELS,
        #                              dtype=tf.uint8)
        image = tf.image.resize_images(image_decoded, [HEIGHT, WIDTH])
        image = tf.cast(image, dtype=tf.uint8)

        return image

    # Run preprocessing function on all images in batch
    raw_image = tf.placeholder(tf.string, shape=[None], name='image_binary')
    images_tensor = tf.map_fn(
        decode_and_resize, raw_image, back_prop=False, dtype=tf.uint8)

    # Cast to float32
    images_tensor = tf.cast(images_tensor, dtype=tf.float32)
    # according to trained model
    #  Run Xception-specific preprocessing to scale images from [0, 255] to [-1, 1]
    # images_tensor = tf.subtract(tf.divide(images_tensor, 127.5), 1)

    return tf.estimator.export.ServingInputReceiver(
        {'input_1': images_tensor},  # The key here needs match the name of your model's first layer
        {'image_bytes': raw_image})   # You can specify the key here, but this is a good default

# The export path contains the name and the version of the model
tf.keras.backend.set_learning_phase(0) # Ignore dropout at inference
model_path = os.path.join(os.getcwd(), "saved_models", "xception.h5")
model = tf.keras.models.load_model(model_path)

estimator_path = os.path.join(os.getcwd(), "tfserving_dogs_cats_estimator")
if not os.path.exists(estimator_path):
    os.makedirs(estimator_path)

# Create an Estimator object
estimator = tf.keras.estimator.model_to_estimator(
   keras_model=model, model_dir=estimator_path)

# https://stackoverflow.com/questions/54615708/exporting-a-keras-model-as-a-tf-estimator-trained-model-cannot-be-found
gen_folder = os.path.join(estimator_path, "keras")
for file_name in os.listdir(gen_folder):
    shutil.copy(os.path.join(gen_folder, file_name), estimator_path)

export_path = os.path.join(os.getcwd(), "tfserving_dogs_cats_models", "1")
estimator.export_savedmodel(
    export_path, serving_input_receiver_fn=serving_input_receiver_fn)

sub_folders = [name for name in os.listdir(export_path)
    if os.path.isdir(os.path.join(export_path, name))]

assert (len(sub_folders) == 1)
sub_folder_path = os.path.join(export_path, sub_folders[0])

for file_name in os.listdir(sub_folder_path):
    shutil.move(os.path.join(sub_folder_path, file_name), export_path)
shutil.rmtree(sub_folder_path)
