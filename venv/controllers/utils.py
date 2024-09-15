def validate_aircraft_image(image_tags):
    valid_tags = ['airplane', 'aircraft', 'plane', 'jet']
    return any(tag.lower() in valid_tags for tag in image_tags)

def is_shabbat(date, location):
    # Implementation of Shabbat checking logic
    # This should use an actual API or library for accurate results
    pass
