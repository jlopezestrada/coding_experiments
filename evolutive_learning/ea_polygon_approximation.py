# Polygon Approximation using evolutive learning
# Goal: find all pixels in the new image to be the same as the reference image
# Individual = a list of N polygons
# Population = Set of Individuals
# Genotype = R, G, B, alpha
# Search Space = 0 to N polygons
# Operators
#    Selection = Selects a number that would continue the generations
#    Crossover = Perform an operation with another number
#    Mutation = Perform an operation with a random number


class Polygon:
    # Attributes
    color_data = []  # r, g, b, alpha channels
    spatial_data = []  # x, y

    # Methods
    def __init__(self, color_data, spatial_data):
        self.color_data = color_data
        self.spatial_data = spatial_data

    @classmethod
    def generate_random(cls):
        return 0


# class Solution:
# Attributes

# Methods
