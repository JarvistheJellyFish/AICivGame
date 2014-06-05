import glob
import random

<<<<<<< HEAD
def random_map(name="", end = "png"):
    images = glob.glob("Images/Perlin/%s*.%s"%(name, end))
=======
def random_map(name=""):
    images = glob.glob("Images/Perlin/%s*.png"%name)
>>>>>>> e9022a423b3b8171706f7d6850695d1f132cd403
    
    for i in images:
        if i[-5] == '2':
            images.remove(i)
            
    random_map = images[random.randint(0, len(images)-1)]
    
<<<<<<< HEAD
    second_map = glob.glob("%s2.%s"%(random_map[:-4], end))
=======
    second_map = glob.glob("%s2.png"%random_map[:-4])
>>>>>>> e9022a423b3b8171706f7d6850695d1f132cd403
    
    if len(second_map) == 0: second_map = None
    else: second_map = second_map[0]
    print random_map, second_map
<<<<<<< HEAD
    return random_map, second_map
=======
    return random_map, second_map
>>>>>>> e9022a423b3b8171706f7d6850695d1f132cd403
