import os
import hashlib

class FileHasher:
    @staticmethod
    def calculate_hash(file_path, algorithm='sha256'):
        """
        Calculates the hash of a file using the specified algorithm.
        :param file_path: Path to the file
        :param algorithm: Hashing algorithm to use (default is 'sha256')
        :return: Hexadecimal hash of the file
        """
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):  # Read the file in chunks
                hash_func.update(chunk)
        return hash_func.hexdigest()

    @staticmethod
    def store_hashes(file_paths, hash_file):
        """
        Stores the hashes of files into a text file.
        :param file_paths: List of file paths to hash
        :param hash_file: Path to the file where hashes will be stored
        """
        with open(hash_file, 'w') as f:
            for file_path in file_paths:
                if os.path.isfile(file_path):
                    file_hash = FileHasher.calculate_hash(file_path)
                    f.write(f"{file_path}:{file_hash}\n")
                else:
                    f.write(f"{file_path}:File not found\n")
        print(f"Hashes have been stored in {hash_file}.")

    @staticmethod
    def compare_hashes(file_paths, hash_file):
        """
        Compares the current hashes of files with the stored hashes in the hash file.
        :param file_paths: List of file paths to hash
        :param hash_file: Path to the file where hashes are stored
        """
        stored_hashes = {}
        if os.path.isfile(hash_file):
            with open(hash_file, 'r') as f:
                for line in f:
                    path, hash_val = line.strip().split(':', 1)

                    stored_hashes[path] = hash_val
        
        

        for file_path in file_paths:
            file_path = str(file_path)
            if os.path.isfile(file_path):
                current_hash = FileHasher.calculate_hash(file_path)
                stored_hash = stored_hashes.get(file_path)
                if stored_hash != current_hash:
                    print(f"File changed: {file_path}")

                else:
                    print(f"File unchanged: {file_path}")
            else:
                print(f"File not found: {file_path}")

    @staticmethod
    def compare_with_hash(file_path, given_hash, algorithm='sha256'):
        """
        Compares the hash of a specific file with a given hash value.
        :param file_path: Path to the file
        :param given_hash: Hash value to compare with
        :param algorithm: Hashing algorithm to use (default is 'sha256')
        """
        if os.path.isfile(file_path):
            current_hash = FileHasher.calculate_hash(file_path, algorithm)
            if current_hash == given_hash:
                print(f"File hash matches the given hash: {file_path}")
            else:
                print(f"File hash does not match the given hash: {file_path}")
        else:
            print(f"File not found: {file_path}")


