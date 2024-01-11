import tensorflow
from keras.applications.resnet import ResNet50, preprocess_input
from keras.layers import GlobalMaxPooling2D
import cv2
import numpy as np
from numpy.linalg import norm
import pickle
from sklearn.neighbors import NearestNeighbors


def prepareModel():
    model = ResNet50(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    model.trainable = False
    model = tensorflow.keras.Sequential([
        model,
        GlobalMaxPooling2D()
    ])

    feature_list = np.array(pickle.load(open("model/featurevector.pkl", "rb")))
    filenames = pickle.load(open("model/filenames.pkl", "rb"))
    return model, feature_list, filenames


def extract_feature(img_arr, model):
    img = cv2.resize(img_arr, (224, 224))
    expand_img = np.expand_dims(img, axis=0)
    pre_img = preprocess_input(expand_img)
    result = model.predict(pre_img).flatten()
    normalized = result/norm(result)
    return normalized


def getSimilarImages(image_arr):
    model, feature_list, filenames = prepareModel()
    neighbors = NearestNeighbors(n_neighbors=6, algorithm="brute", metric="euclidean")
    neighbors.fit(feature_list)

    distance, indices = neighbors.kneighbors([extract_feature(image_arr, model)])

    return indices[0][1:6], distance, filenames
