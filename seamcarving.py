class seamcarving:
    def __init__(self):
        self.seam = []

    # compute the energy of a pixel at (x, y)
    def compute_energy(self, image, x, y):
        y_max, x_max = len(image), len(image[0])
        distance_sum = 0
        neighbor_count = 0

        # find up to 8 neighbors for each pixel
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                p2_x = x + i
                p2_y = y + j
                # if the neighbors are within the bounds of the image
                if 0 <= p2_x < x_max and 0 <= p2_y < y_max:
                    neighbor_count += 1
                    distance = 0
                    # 3D Euclidian distance formula to find average difference between pixel and neighbors
                    for c in range(3):
                        distance += (image[p2_y][p2_x][c] - image[y][x][c]) ** 2
                    distance = distance ** 0.5
                    distance_sum += distance

        if neighbor_count > 0:
            energy = distance_sum / neighbor_count
        else:
            energy = 0
        return energy