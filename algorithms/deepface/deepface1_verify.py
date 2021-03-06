# -*- coding: utf-8 -*-
"""Deepface1_verify.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YR47_Lzvm4oSEfNOuQAV0CM4Sgy9Ua5n
"""

from google.colab import drive
drive.mount('/content/gdrive')

!pip install deepFace
 !pip install termcolor #for color print

from deepface import DeepFace
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from termcolor import colored #for color print
import json
import os

#consts
dataset_path = "/content/gdrive/MyDrive/MIT_dataset/images/"
file_extension = ".jpg"
result_map = dict()
distance_map = dict()

models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID" , "ArcFace", "Dlib"]
metrics = ["cosine", "euclidean", "euclidean_l2"]

def init():
  global result_map, distance_map

  for filename in sorted(os.listdir(dataset_path)):
    key = filename.split('.')[0] #get file names without 
    
    print("adding ", key, " to map...")
    result_map.update({key: {} })
    distance_map.update({key: {}})
  # print(result_map)

def verify(img1_path, img2_path, model_name, model, distance_metric):
  
  result = DeepFace.verify(img1_path, img2_path, model_name=model_name, model=model, distance_metric=distance_metric)

  # print(colored("================================", 'red'))
  # print(colored("Model name: ", 'green'), model_name)
  # print(colored("Metric name: ", 'green'), distance_metric)
  print(colored("Result: ", 'green'), result)
  # print(colored("================================", 'red'))

  return result["verified"], round(result["distance"], 2) # True / False --- distance

def print_info(key1, key2, result, distance, model_name):

  # print(colored("===========================================================================================", 'red'))
  print("key1:", colored(key1, 'green'), "key2:", colored(key2, 'green'), "distance:", colored(distance, 'green'), end=" ")

  if result:
    print("result:", (colored(result, 'green')), "model_name:", colored(model_name, 'green'))
  else:
    print("result:", (colored(result, 'red')), "model_name:", colored(model_name, 'green'))

  # print(colored("===========================================================================================", 'red'))

def show_final_results(model_name, metric_name, map):

  print("========================================FINAL RESULTS========================================")
  print("MODEL:", model_name, "METRIC:", metric_name)

  for key, content in sorted (map.items()):
    score = None
    if content is not None:
      score = content.values()

    print(key, ":", score)

def clear_maps():
  global result_map, distance_map

  print(colored("clearing map...", 'red'))
  for key in result_map.keys():
    result_map.update({key: {} })
    distance_map.update({key: {}})

def add_results(models, metrics):
  global result_map, distance_map

  for model_name in models:
    loaded_model=DeepFace.build_model(model_name)

    for metric_name in metrics:
    
      clear_maps()

      for key1 in result_map.keys():

        complete_file_path_1 = dataset_path + key1 + file_extension

        for key2 in result_map.keys():
          
          #same key case
          if key1 == key2:
            result_map[key2][key1] = "True"
            distance_map[key2][key1] = 0.00
            continue

          #check to see if value at key1 already exists
          #check to see if value at key1 at key2 is {}
          if not result_map[key1] or not result_map[key1].get(key2):
            
            complete_file_path_2 = dataset_path + key2 + file_extension

            result, distance = verify(complete_file_path_1, complete_file_path_2, model_name, loaded_model, metric_name)
            
            print_info(key1, key2, result, distance, model_name)


            # add result to map - key1
            result_map[key1][key2] = str(result)
            
            # add result to map - key2 
            if not result_map[key2].get(key1):
              result_map[key2][key1] = str(result)
            
            # add distance to map - key1
            distance_map[key1][key2] = distance
             
            # add distance to map - key2
            if not distance_map[key2].get(key1):
              distance_map[key2][key1] = distance
            
          
      print("RESULT MAP:")
      show_final_results(model_name, metric_name, result_map)
      print("DISTANCE MAP:")
      show_final_results(model_name, metric_name, distance_map)

init()

#running time to high for:
# add_results(models, metrics) 

#could be use separately like:
# add_results(["VGG-Face"], ["cosine"])  #done
# add_results(["VGG-Face"], ["euclidean"])  #done
# add_results(["VGG-Face"], ["euclidean_l2"])  #done

# add_results(["Facenet"], ["cosine"])   #done
# add_results(["Facenet"], ["euclidean"])  #done
# add_results(["Facenet"], ["euclidean_l2"])  #done

# add_results(["OpenFace"], ["cosine"])   #done
# add_results(["OpenFace"], ["euclidean"])   #done
# add_results(["OpenFace"], ["euclidean_l2"])  #done

# add_results(["DeepFace"], ["cosine"])  #done
# add_results(["DeepFace"], ["euclidean"])  #done
# add_results(["DeepFace"], ["euclidean_l2"])  #done

# add_results(["DeepID"], ["cosine"])   #done
# add_results(["DeepID"], ["euclidean"])   #done
# add_results(["DeepID"], ["euclidean_l2"])  #done

# add_results(["ArcFace"], ["cosine"])  #done
# add_results(["ArcFace"], ["euclidean"])  #done
# add_results(["ArcFace"], ["euclidean_l2"])  #done

# add_results(["Dlib"], ["cosine"])  #done
# add_results(["Dlib"], ["euclidean"])  #done
# add_results(["Dlib"], ["euclidean_l2"]) #done