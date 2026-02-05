# Lab02HashingProgram
# Overview:
To demonstrate hashing you will write a program from scratch that is able to hash any file in a chosen directory and store a list of files and their hashes in a .json file.
Additionally, your program will be able to verify the hash values of files in a directory based on the hash table you generated.
When your program is run you should give the user two options, 1 for generating a new hash table, and 2 for verifying hashes. If the user selects generate a new hash table, your program will prompt them to enter a directory path to where the files are that need to be hashed are. For example, if a user enters “/Docs/3200Notes”, your program will navigate to that directory and calculate the hash value for the files within. Your program will generate a hash table as .json file that stores the file path and hash value for each file within the directory. This will be stored as filepath and hash
