# Imports 
import time 
import praw
import requests   
import time
import os 

# Initialize praw - which we use to scrape reddit 
reddit = praw.Reddit(
    client_id="1r19Ty7tWw4-2BnmHZJZRg",
    client_secret="R0J2Q0NRVCjY_KHvYsfIuXKxgOS5iQ",
    password="FvckR3ddit33!!!",
    user_agent="fungus_amongus",
    username="ruxasaurus_rex",
)

# The count of mushrooms we got from downloading the original dataset 
mushroom_species_count = {
 'mycena leaiana': 507, 
 'laetiporus sulphureus': 566,
 'trametes versicolor': 1251,
 'coprinus comatus': 813,
 'ganoderma oregonense': 731,
 'chlorophyllum molybdites': 556,
 'mycena haematopus': 531,
 'lycoperdon perlatum': 530}

# The total number of images we have downloaded 
total_images_counter = 0 

# Write to a log 
with open("C:\\Users\\rkabealo\\Documents\\School\\AU22\\NN\\PJ2\\reddit_download_log.txt", 'a') as f:
    # For each species in the species we downloaded 
    for species in mushroom_species_count.keys(): 
        print(f"--- {species} ---")
        f.write(f"--- {species} ---" + "\n")

        # Count how many images we obtained 
        species_images_counter = 0 
        # Create a folder to store them in 
        species_name_properly_formatted = species.replace(" ", "_")
        path_to_species_folder = "C:\\Users\\rkabealo\\Documents\\School\\AU22\\NN\\PJ2\\reddit_dataset\\" + species_name_properly_formatted
        os.makedirs(path_to_species_folder, exist_ok = True)
        
        # Search all of reddit for this species 
        for post in reddit.subreddit("Fungi+mycology+MushroomPorn+mycoporn+Mushrooms+mushroomID+MagicMushroomHunters+ShroomID+whatisthismushroom+MushroomGrowers").search(species):
            print(f"--- {species_images_counter} ---")
            f.write(f"--- {species_images_counter} ---" + "\n")
            print(post.url)
            f.write(post.url + "\n")

            # If its a gallery of images, download each image from the gallery 
            if ".jpg" not in post.url:
                try: 
                    submission_items = post.media_metadata.items()
                    
                    # For each item in the gallery 
                    for item in submission_items: 
                        url = item[1]['p'][0]['u']
                        url = url.split("?")[0].replace("preview", "i")

                        mushroom_species_count[species] = mushroom_species_count[species]+1
                        filename = species_name_properly_formatted + "_" + str(mushroom_species_count[species]).zfill(5) + ".jpg"

                        with open(path_to_species_folder + "\\" + filename, 'wb') as fs:
                            fs.write(requests.get(url).content)
                        
                        print(f"> Downloaded {filename} from {url} at {time.asctime(time.localtime())}")
                        f.write(f"> Downloaded {filename} from {url} at {time.asctime(time.localtime())}" + "\n")
                        species_images_counter += 1 
                        total_images_counter += 1

                        # Quit downloading images once we've reached 300 for a species 
                        if species_images_counter > 300: 
                            print(f"Downloaded {species_images_counter} for {species}")
                            f.write(f"Downloaded {species_images_counter} for {species}" + "\n")
                            print(f"Downloaded {total_images_counter} images total")
                            f.write(f"Downloaded {total_images_counter} images total" + "\n")
                            break
                except: 
                    print("No images")
                    f.write("No images \n")
            else:
                # If "jpg" is in the URL then this is just a URL that points directly to the picture - download it directly
                url = post.url

                mushroom_species_count[species] = mushroom_species_count[species]+1
                filename = species_name_properly_formatted + "_" + str(mushroom_species_count[species]).zfill(5) + ".jpg"

                with open(path_to_species_folder + "\\" + filename, 'wb') as fss:
                    fss.write(requests.get(url).content)

                print(f"> Downloaded {filename} from {url} at {time.asctime(time.localtime())}")
                f.write(f"> Downloaded {filename} from {url} at {time.asctime(time.localtime())}" + "\n")
                species_images_counter += 1 
                total_images_counter += 1 

                # Quit downloading images once we've reached 300 for a species 
                if species_images_counter > 300: 
                    print(f"Downloaded {species_images_counter} for {species}")
                    f.write(f"Downloaded {species_images_counter} for {species}" + "\n")
                    print(f"Downloaded {total_images_counter} images total")
                    f.write(f"Downloaded {total_images_counter} images total" + "\n")
                    break
        
        print(f"Downloaded {species_images_counter} for {species}")
        f.write(f"Downloaded {species_images_counter} for {species}" + "\n")
        print(f"Downloaded {total_images_counter} images total")
        f.write(f"Downloaded {total_images_counter} images total" + "\n")
        

    