import time
from PIL import Image
from seamcarving import seamcarving


def load_image(filepath):
    fp = Image.open(filepath)
    pixels = fp.load()
    w, h = fp.size
    image_data = [[[0 for _ in range(3)] for _ in range(w)] for _ in range(h)]
    for i in range(w):
        for j in range(h):
            image_data[j][i] = list(pixels[i, j][:3])
    return image_data, w, h


def main():
    # Ask the user for the image filename
    image_filename = input("Enter the image filename: ")

    # Load image and initialize seam carving
    image_data, w, h = load_image(image_filename)
    sc = seamcarving()

    # Ask the user for the target width
    target_width = int(input("Enter the target width: "))

    # Ensure the target width is valid
    if target_width >= w:
        print("Error: Target width should be smaller than the original width.")
        return

    # Loop to continuously remove seams
    start = time.time()
    while w > target_width:
        weight = sc.compute(image_data)
        print(f"Current width: {w}, Seam weight: {weight}")
        image_data = sc.remove_seam(image_data)
        w -= 1

    end = time.time()
    print(f"Resizing completed in {end - start:.2f} seconds.")

    # Save or show the resized image
    resized_image = Image.new("RGB", (target_width, h))
    for y in range(h):
        for x in range(target_width):
            resized_image.putpixel((x, y), tuple(image_data[y][x]))
    resized_image.show()
    # resized_image.save("resized_duck.png")

if __name__ == "__main__":
    main()