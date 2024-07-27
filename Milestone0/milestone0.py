import csv

def load_care_areas(filename):
    care_areas = []
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            #next(reader) #To skip the header of the csv file
            for row in reader:
                if row:  
                    care_areas.append({
                        'ID': int(row[0]),
                        'x1': float(row[1]),
                        'x2': float(row[2]),
                        'y1': float(row[3]),
                        'y2': float(row[4])
                    })
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred while loading care areas: {e}")
    return care_areas

def load_metadata(filename):
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            metadata = list(reader)
            if len(metadata) < 1:
                raise ValueError("The metadata file is empty.")
            main_field_size = float(metadata[0][0])
            sub_field_size = float(metadata[0][1])
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred while loading metadata: {e}")
    return main_field_size, sub_field_size

def save_main_fields(filename, main_fields):
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            #writer.writerow(['ID', 'x1', 'x2', 'y1', 'y2'])
            for i, field in enumerate(main_fields):
                writer.writerow([i, field['x1'], field['x2'], field['y1'], field['y2']])
    except Exception as e:
        print(f"An error occurred while saving main fields: {e}")

def save_sub_fields(filename, sub_fields):
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            #writer.writerow(['ID', 'x1', 'x2', 'y1', 'y2', 'MF_ID'])
            for i, field in enumerate(sub_fields):
                writer.writerow([i, field['x1'], field['x2'], field['y1'], field['y2'], field['MF_ID']])
    except Exception as e:
        print(f"An error occurred while saving sub fields: {e}")

def generate_fields(care_areas, main_field_size, sub_field_size):
    main_fields = []
    sub_fields = []
    
    for care_area in care_areas:
         mf_x1, mf_y1 = care_area['x1'], care_area['y1']
         mf_x2, mf_y2 = mf_x1 + main_field_size, mf_y1 + main_field_size
         main_fields.append({'x1': mf_x1, 'x2': mf_x2, 'y1': mf_y1, 'y2': mf_y2})
       
         for sub_x in range(int(mf_x1), int(care_area['x2']), int(sub_field_size)):
             for sub_y in range(int(mf_y1), int(care_area['y2']), int(sub_field_size)):
                 sf_x1, sf_y1 = sub_x, sub_y
                 sf_x2, sf_y2 = sf_x1 + sub_field_size, sf_y1 + sub_field_size
                 if sf_x2 <= mf_x2 and sf_y2 <= mf_y2:
                     sub_fields.append({'x1': sf_x1, 'x2': sf_x2, 'y1': sf_y1, 'y2': sf_y2, 'MF_ID': len(main_fields)-1})
    
    return main_fields, sub_fields

def main():
    care_areas = load_care_areas(r'Milestone 0\CareAreas.csv')
    main_field_size, sub_field_size = load_metadata(r'Milestone 0\metadata.csv')
    main_fields, sub_fields = generate_fields(care_areas, main_field_size, sub_field_size)
    for i in care_areas:
        print(i)
    
    save_main_fields(r'Milestone 0\MainFields.csv', main_fields)
    save_sub_fields(r'Milestone 0\SubFields.csv', sub_fields)

if __name__ == "__main__":
    main()
