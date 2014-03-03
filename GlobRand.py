import glob
import random

def random_map(name=""):
    images = glob.glob("Images/Perlin/%s*.png"%name)
    
    for i in images:
        if i[-5] == '2':
            images.remove(i)
            
    random_map = images[random.randint(0, len(images)-1)]
    
    second_map = glob.glob("%s2.png"%random_map[:-4])
    
    if len(second_map) == 0: second_map = None
    else: second_map = second_map[0]
    print random_map, second_map
    return random_map, second_map
