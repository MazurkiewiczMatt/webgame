def get_trait_description(degree, trait):
    # Define the mappings
    trait_mapping = {
        "Dedication": [
            (0, 20, "Dormant"),
            (20, 40, "Aimless"),
            (40, 60, "Neutral"),
            (60, 80, "Radiant"),
            (80, 100, "Maniac")
        ],
        "Faith": [
            (0, 20, "Nihilist"),
            (20, 40, "Cynical"),
            (40, 60, "Neutral"),
            (60, 80, "Confident"),
            (80, 95, "Prophet"),
            (95, 100, "Messiah")
        ],
        "Degeneracy": [
            (0, 20, "Holy"),
            (20, 40, "Pure"),
            (40, 60, "Neutral"),
            (60, 80, "Rebellious"),
            (80, 95, "Menace"),
            (95, 100, "Wicked")
        ]
    }

    # Get the corresponding descriptions for the trait
    descriptions = trait_mapping.get(trait)

    if descriptions is None:
        return "Invalid trait"

    # Find the appropriate description based on the degree
    for min_val, max_val, description in descriptions:
        if min_val <= degree < max_val:
            return description
    return "Invalid degree"
