import json

# Replace 'your_file.json' with the path to your actual file
file_path = r'C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\ONCE Data\000076.json'

# Open and load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)
    # Initialize a list to hold all "annos" data
    all_annos = []

    # Assuming the structure includes a 'frames' key at the top level
    if 'frames' in data:
        for frame in data['frames']:
            # Check if 'annos' exists
            if 'annos' in frame:
                # Add the "annos" data to our list
                all_annos.append(frame['annos'])

    # Print or return the collected "annos" data
    print(all_annos)
    # Or return all_annos if using within a function
