import imageio

# draw pixelarts on "https://www.pixilart.com/draw#"
# then download bit image.
# use this to convert to list of numbers.

def parse_bit_image(bitimagelocation):
    bitimage = imageio.imread(bitimagelocation)
    dots = []
    ylength,xlength,_ = bitimage.shape
    for x in range(xlength):
        for y in range(ylength):
            if bitimage[y,x][-1] == 255:
                dots.append((x,y))
    for i in range(len(dots)//10+1):
        print(*dots[i*10:10*(i+1)],'',sep=',')

    return dots


dot = parse_bit_image('/Users/hui/Documents/Scripts/micropython/pixelarts/sun2.png')
