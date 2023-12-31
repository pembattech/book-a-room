from django.utils.text import slugify
import string
import random


# Function to generate a random string of length N
def generate_random_string(N):
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    return res

# Function to generate a unique slug based on the given text
def generate_slug(text):
    new_slug = slugify(text)  # Convert the text to a slug using Django's slugify function

    from hotel.models import Hotel
    if Hotel.objects.filter(slug=new_slug).first():
        # If it exists, append a random string to the text and recursively generate a new slug
        return generate_slug(text + "_" + generate_random_string(3))
    
    # If the slug is unique, return it
    return new_slug