import tensorflow as tf
import numpy as np
from .common import *

def initialize(gan, d_vars, g_vars):
    d_loss = gan.graph.d_loss
    g_loss = gan.graph.g_loss
    config = gan.config
    g_lr = np.float32(config['trainer.adam.generator.lr'])
    d_lr = np.float32(config['trainer.adam.discriminator.lr'])
    d_beta1 = np.float32(config['trainer.adam.discriminator.beta1'])
    d_beta2 = np.float32(config['trainer.adam.discriminator.beta2'])
    d_epsilon = np.float32(config['trainer.adam.discriminator.epsilon'])
    g_beta1 = np.float32(config['trainer.adam.generator.beta1'])
    g_beta2 = np.float32(config['trainer.adam.generator.beta2'])
    g_epsilon = np.float32(config['trainer.adam.generator.epsilon'])
    gan.graph.d_vars = d_vars
    g_optimizer = tf.train.AdamOptimizer(g_lr).minimize(g_loss, var_list=g_vars)
    d_optimizer = tf.train.AdamOptimizer(d_lr).minimize(d_loss, var_list=d_vars)
    return g_optimizer, d_optimizer

iteration = 0
def train(gan):
    sess = gan.sess
    config = gan.config
    x_t = gan.graph.x
    g_t = gan.graph.g
    d_log_t = gan.graph.d_log
    g_loss = gan.graph.g_loss
    d_loss = gan.graph.d_loss
    d_fake_loss = gan.graph.d_fake_loss
    d_real_loss = gan.graph.d_real_loss
    g_optimizer = gan.graph.g_optimizer
    d_optimizer = gan.graph.d_optimizer
    d_class_loss = gan.graph.d_class_loss
    d_vars = gan.graph.d_vars

    _, d_cost, d_log = sess.run([d_optimizer, d_loss, d_log_t])
    # in WGAN paper, values are clipped.  This might not work, and is slow.
    #clip = [tf.assign(d,tf.clip_by_value(d, -0.1, 0.1))  for d in d_vars]
    #sess.run(clip)

    _, g_cost,d_fake,d_real,d_class = sess.run([g_optimizer, g_loss, d_fake_loss, d_real_loss, d_class_loss])
    print("%2d: g cost %.2f d_loss %.2f d_real %.2f d_class %.2f d_log %.2f" % (iteration, g_cost,d_cost, d_real, d_class, d_log ))

    global iteration
    iteration+=1

    return d_cost, g_cost


