import sys
sys.path.append('/home/ruiliu/Development/tf-exp/models/research/slim')
sys.path.append('/home/ruiliu/Development/tf-exp/models/official')

import tensorflow as tf
from nets.mobilenet import mobilenet_v2
from datasets import imagenet
import timeit

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--grow", action="store_true", help="Allowing GPU memory growth")
args = parser.parse_args()

tf.reset_default_graph()

# For simplicity we just decode jpeg inside tensorflow.
# But one can provide any input obviously.
file_input = tf.placeholder(tf.string, ())

image = tf.image.decode_jpeg(tf.read_file(file_input))

images = tf.expand_dims(image, 0)
images = tf.cast(images, tf.float32) / 128.  - 1
images.set_shape((None, None, None, 3))
images = tf.image.resize_images(images, (224, 224))

# Note: arg_scope is optional for inference.
with tf.contrib.slim.arg_scope(mobilenet_v2.training_scope(is_training=False)):
    logits, endpoints = mobilenet_v2.mobilenet(images)

# Restore using exponential moving average since it produces (1.5-2%) higher 
# accuracy
ema = tf.train.ExponentialMovingAverage(0.999)
vars = ema.variables_to_restore()

saver = tf.train.Saver(vars)

checkpoint = "/home/ruiliu/Development/tf-exp/ckpts/mobilenet2/mobilenet_v2_1.0_224.ckpt"

if args.grow:
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
        saver.restore(sess,  checkpoint)
        start = timeit.default_timer()
        x = endpoints['Predictions'].eval(feed_dict={file_input: '../data/img.jpg'})
        stop = timeit.default_timer()
        print('Inference Time: ', stop - start)
else: 
    with tf.Session() as sess:
        saver.restore(sess,  checkpoint)
        start = timeit.default_timer()
        x = endpoints['Predictions'].eval(feed_dict={file_input: '../data/img.jpg'})
        stop = timeit.default_timer()
        print('Inference Time: ', stop - start)

label_map = imagenet.create_readable_names_for_imagenet_labels()
print("Top 1 prediction: ", x.argmax(),label_map[x.argmax()], x.max())

