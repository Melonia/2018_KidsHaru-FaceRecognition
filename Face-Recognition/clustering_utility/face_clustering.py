from sklearn.cluster import DBSCAN
import pickle
import numpy as np
import os
import signal
import sys
import cv2
import model_custom
from picture_utility import picture_class as pc

def clustering(data2):
    cnt = 0
    name = []
    img = []
    encodings = []

    cnt = 0
    for i in range(data2.getLen()):
        if data2.getEncoding(i) != []:
            for j in range(len(data2.getEncoding(i))):
                # print(data2.getPictureCut(i)[j])
                img.append(data2.getPictureCut(i)[j])
                encodings.append(data2.getEncoding(i)[j])

    # for i in range(len(img)):
        #print(img[i].split('/')[4])
    
    # cluster the embeddings
    clt = DBSCAN(metric="euclidean")
    clt.fit(encodings)

    # label 결정
    label_ids = np.unique(clt.labels_)
    num_unique_faces = len(np.where(label_ids > -1)[0])
    print("clustered %d unique faces." % num_unique_faces)
    # print(len(label_ids))

    
    path = "./clustering_utility/"
    for label_id in label_ids:
        dir_name = "ID%d" % label_id
        print(dir_name)

        if not os.path.isdir(path + dir_name):
            os.mkdir(path + dir_name)

        # find all indexes of label_id
        indexes = np.where(clt.labels_ == label_id)[0]
        # print(indexes)

        # save face images
        for i in indexes:
            image = cv2.imread(img[i])
        
            url_path = path + dir_name + "/" + img[i].split('/')[3] + "_" + img[i].split('/')[4]
            # print(url_path, img[i])
            # print(i)

            cv2.imwrite(url_path, image)

    print('clustering done')
