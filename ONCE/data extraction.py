import json

# Replace 'your_file.json' with the path to your actual file
file_path = r'C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\ONCE Data\000076.json'

# Open and load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

    # Initialize a list to hold all "names" lists
    all_names = []

    # Assuming the structure includes a 'frames' key at the top level
    if 'frames' in data:
        for frame in data['frames']:
            # Check if 'annos' exists and then if 'names' is in 'annos'
            if 'annos' in frame and 'names' in frame['annos']:
                # Add the "names" list to our collection
                all_names.append(frame['annos']['names'])
    dictionary = {}
    for section in all_names:
        for object in section:
            if object in dictionary:
                dictionary[object] += 1
            else:
                dictionary[object] = 0

    # Print or return the collected "names" lists
    #print(all_names)
    print(dictionary)
    # Or return all_names if using within a function
