import os
import random

class FileShredder:
    @staticmethod
    def overwrite_file(file_path, passes):
        """
        Overwrites the file with random and pattern data for a specified number of passes.
        :param file_path: Path to the file to be shredded
        :param passes: Number of passes to overwrite the file
        """
        file_size = os.path.getsize(file_path)
        
        with open(file_path, 'r+b') as f:
            for _ in range(passes):
                f.seek(0)  # Go to the start of the file
                if _ % 2 == 0:
                    # Write random data over the entire file size
                    f.write(bytes([random.randint(0, 255)] * file_size))
                else:
                    # Write pattern data (0x00 or 0xFF) over the entire file size
                    pattern = bytes([0x00] * file_size) if _ % 4 == 0 else bytes([0xFF] * file_size)
                    f.write(pattern)
                f.flush()  # Ensure data is written to the file

    @staticmethod
    def shred_files(file_paths, passes=7):
        """
        Shreds a list of files to make them unrecoverable based on DoD 5220.22-M standards.
        :param file_paths: List of file paths to be shredded
        :param passes: Number of passes to overwrite the files
        """
        for file_path in file_paths:
            if os.path.isfile(file_path):
                # Overwrite the file
                FileShredder.overwrite_file(file_path, passes)
                # Delete the file
                os.remove(file_path)
                print(f"File {file_path} has been shredded and deleted.")
            else:
                print(f"File {file_path} does not exist.")

