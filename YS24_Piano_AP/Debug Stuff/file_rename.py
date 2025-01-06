import os
import string

def sanitize_filenames(directory):
    # Get all files in the specified directory
    for filename in os.listdir(directory):
        # Full path to the file
        full_path = os.path.join(directory, filename)
        
        # Skip directories
        if not os.path.isfile(full_path):
            continue

        # Replace non-alphabet characters with 'x'
        allowed_chars = string.ascii_letters + string.digits
        sanitized_name = ''
        for char in filename:
            if char in allowed_chars: 
                sanitized_name = sanitized_name + char
            elif char == '(' or char == ')':
                sanitized_name = sanitized_name + char
            elif (char == '-') or (char == ' ') or (char == '.'):
                sanitized_name = sanitized_name + char
            elif (char == "'") or (char == ","):
                sanitized_name = sanitized_name
            elif (char == "&"):
                sanitized_name = sanitized_name + "and"
            else: 
                sanitized_name = sanitized_name + 'x'
        
            #sanitized_name = ''.join(char if char in string.ascii_letters else 'x' for char in filename)

        sanitized_path = os.path.join(directory, sanitized_name)
        
        #Rename the file, if there has been a change... 
        if sanitized_name != filename:
            print("")
            # If the sanitized file already exists, delete the original
            if os.path.exists(sanitized_path):
                os.remove(sanitized_path)
                print(f"Deleted duplicate: {sanitized_path}")

            print("Santised Name ", sanitized_name)
            print("OG Name ", filename)
            try:
                os.rename(full_path, sanitized_path)
                print(f"Renamed: {filename} -> {sanitized_name}")
            except Exception as e:
                print(f"Error processing file '{filename}': {e}")
            
            """
            print(f"Renamed: {filename} -> {sanitized_name}")
            print("")
            print("Santised Name ", sanitized_name)
            print("OG Name ", filename)
            input_val = input("What would you like to do...")
            if input_val == 'y':
                new_path = os.path.join(directory, sanitized_name)
                try:
                    os.rename(full_path, new_path)
                    print(f"Renamed: {filename} -> {sanitized_name}")
                except Exception as e:
                    print(f"Error processing file '{filename}': {e}")
            """

# Example usage
directory_path = "piano/YS24_Piano_AP/midi_songs"  # Replace with the target directory path
sanitize_filenames(directory_path)