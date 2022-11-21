# Imports 
import pandas as pd 
import matplotlib.pyplot as plt
import time 
import os
import requests
from PIL import Image
import io

# Create a directory to store everything 
os.makedirs("C:\\Users\\rkabealo\\Documents\\School\\AU22\\NN\\PJ2\\mo_ml_species_dataset", exist_ok=True)

# Grab the CSV file from Mushroom Observer detailing where the images are located 
os.system(f"wget -O C:\\Users\\rkabealo\\Documents\\School\\AU22\\NN\\PJ2\\MO_ML_Images_And_Names.csv https://docs.google.com/spreadsheets/d/1aQSmLlthx99pCt_IS6aHyhZdn_hUiv3EBLbf4h3Zg7s/export?gid=661544393&format=csv")

# Process the CSV from Mushroom Observer so we can obtain only entries we want to download 
original_dataset = pd.read_csv("C:\\Users\\rkabealo\\Documents\\School\\AU22\\NN\\PJ2\\mo_ml_species_dataset\\MO_ML_Images_And_Names.csv", delimiter=",")
original_dataset.loc[pd.isnull(original_dataset[["name"]]).any(axis=1)]
original_dataset = original_dataset.dropna(subset=["name"])
species_only_dataset = original_dataset[original_dataset["name"].map(lambda x: len(x.split(" ")) > 1)]
species_only_above_500_dataset = species_only_dataset[species_only_dataset["name"].map(species_only_dataset["name"].value_counts()) >= 500]

name_map = {"laetiporus sulphureus":"chicken-of-the-woods",
"ganoderma oregonense":"western varnished conk",
"trametes versicolor":"turkey tail",
"coprinus comatus":"shaggy ink cap",
"mycena haematopus":"bleeding fairy helmet",
"mycena leaiana": "orange mycena",
"lycoperdon perlatum":"common puffball",
"chlorophyllum molybdites":"vomiter"}

# A dictionary to keep track of how many of each species we've downloaded 
mushroom_species = {}

# A dictionary to store if we have downloaded any images unsuccessfully 
bad_codes = {}

# For each row in the dataset containing images we're interested in 
for row in species_only_above_500_dataset.iterrows():
  # Get the URL of the image 
  row_number = row[0]
  url = row[1]["image"]
  # Get the filename and extension of the image  
  filename = url.split("/")[-1]
  ext = filename.split(".")[-1]

  # Keep track of what species we've downloaded an image for and which number this one is 
  species_name = row[1]["name"].lower().replace(" ", "_")
  if species_name not in mushroom_species.keys(): 
    mushroom_species[species_name] = 1
  else: 
    mushroom_species[species_name] = mushroom_species[species_name] + 1 
  
  # Change the filename to avoid downloading something with the same name: 
  filename = species_name + "_" + str(mushroom_species[species_name]).zfill(5) + "." + ext

  # Get the image 
  code = os.system(f"wget --output-document=C:\\Users\\rkabealo\\Documents\\School\\AU22\\NN\\PJ2\\mo_ml_species_dataset\\{filename} {url}")

  # If our download wasn't successful,  store this information for later 
  if code != 0: 
    bad_codes[url] = code 

  # Display that we've downloaded an image to the user 
  print(f"> Downloaded {filename} from {url} at {time.asctime(time.localtime())} with Code {code} from Row {row_number}")

