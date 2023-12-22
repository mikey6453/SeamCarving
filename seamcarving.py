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
    

    def compute(self, image):
        y_max, x_max = len(image), len(image[0])

        # create matrix of energies and initialize dp matrix
        energy = [[self.compute_energy(image, x, y) for x in range(x_max)] for y in range(y_max)]
        dp = [[0 for _ in range(x_max)] for _ in range(y_max)]

        # initialize first row of dp matrix with associated energies
        for x in range(x_max):
            dp[0][x] = energy[0][x]

        # calculate the minimum energies for each row in dp matrix
        for y in range(1, y_max):
            for x in range(0, x_max):
                # find minimum energy from top left, top, and top right
                min_energy = dp[y - 1][x]
                if x > 0:
                    min_energy = min(min_energy, dp[y - 1][x - 1])
                if x < x_max - 1:
                    min_energy = min(min_energy, dp[y - 1][x + 1])
                dp[y][x] = energy[y][x] + min_energy

        min_energy = float('inf')
        min_energy_column_index = 0

        # find where the minimum energy seam ends by comparing energies of bottom row
        for column_index in range(x_max):
            current_energy = dp[-1][column_index]
            if current_energy < min_energy:
                min_energy = current_energy
                min_energy_column_index = column_index
        min_seam_end = min_energy_column_index

        self.seam = [min_seam_end]
        for y in range(y_max - 1, 0, -1):
            x = self.seam[-1]
            min_x = max(x - 1, 0)  # cannot be lower than 0

            # Check the pixels above, upper left, and upper right within bounds and finds best seam
            for dx in range(max(x - 1, 0), min(x + 2, x_max)):
                if dp[y - 1][dx] < dp[y - 1][min_x]:
                    min_x = dx
            self.seam.append(min_x)
        self.seam.reverse()  # reverse seam

        return dp[-1][min_seam_end]
    

    def remove_seam(self, image):
        y_max, x_max = len(image), len(image[0])
        new_image = [[[0 for _ in range(3)] for _ in range(x_max - 1)] for _ in range(y_max)]

        for y in range(y_max):
            seam_x = self.seam[y]
            for x in range(x_max - 1):
                new_image[y][x] = image[y][x + (x >= seam_x)]

        return new_image

    def getSeam(self):
        return self.seam