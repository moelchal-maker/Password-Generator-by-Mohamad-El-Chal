'''
Password generator
A simple password generator that creates a random password based on user-defined criteria.

'''
import random, string, time, os, sys

# Base directory (script location)
baseDir = os.path.dirname(os.path.abspath(__file__))


#Word list loader
def loadWords(fileName=None):
    """Load words from a file.

    If `filename` is None the function will look for
    `top_english_nouns_lower_100000.txt` next to the script.
    """
    if fileName is None:
        fileName = os.path.join(baseDir, "top_english_nouns_lower_100000.txt")
    else:
        fileName = os.path.abspath(fileName)

    try:
        with open(fileName, "r") as fileHandle:
            return [word.strip() for word in fileHandle if word.strip()]
    except FileNotFoundError:
        print(f"Error: word list file not found: {fileName}")
        print("Provide the path as the first command-line argument or place the file next to the script.")
        sys.exit(1)


#The current time formatter to 
def currentTime():
    return time.strftime("%A, %Y-%m-%d %H:%M:%S", time.localtime())


# Write password to file
def writePassword(category, password):
    # Write a password to a category directory's Generated_Passwords.txt file.
    cat = category.lower()
    if cat.startswith("mem"):
        dirName = "Memorable"
    elif cat.startswith("rand"):
        dirName = "Random"
    elif cat.startswith("cust") or cat.startswith("man") or cat.startswith("user"):
        dirName = "Custom"
    else:
        dirName = "Random"

    dirPath = os.path.join(baseDir, dirName)
    os.makedirs(dirPath, exist_ok=True)

    filePath = os.path.join(dirPath, "Generated_Passwords.txt")
    with open(filePath, "a", encoding="utf-8") as fileHandle:
        fileHandle.write(f"{password} | Created: {currentTime()}\n")


#Rememberable password generator
def generateMemorable(words, numWords, caseType):
    selectedWords = random.sample(words, numWords)
    finalWords = []

    for word in selectedWords:
        digit = str(random.randint(0, 9))

        if caseType == "upper":
            word = word.upper()
        elif caseType == "title":
            word = word.title()
        # lower case is default (file is already lowercase)

        finalWords.append(word + digit)

    password = "-".join(finalWords)
    writePassword("Memorable", password)
    return password


# Random password generator
def generateRandom(length, includePunctuation, bannedChars):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits

    if includePunctuation:
        characters += string.punctuation

    characters = "".join(c for c in characters if c not in bannedChars)

    password = "".join(random.choice(characters) for _ in range(length))
    writePassword("Random", password)
    return password


# Choosing password type and what to generate 
def passwordGenerator(words):
    passwordType = input("Choose password type (memorable/random/manual): ").lower()

    if passwordType == "memorable":
        numWords = int(input("Number of words: "))
        caseType = input("Case (lower/upper/title): ").lower()
        password = generateMemorable(words, numWords, caseType)

    elif passwordType == "random":
        length = int(input("Password length: "))
        includePunctuation = input("Include punctuation? (yes/no): ").lower() == "yes"
        bannedChars = input("Characters to exclude: ")
        password = generateRandom(length, includePunctuation, bannedChars)

    elif passwordType in ("manual", "enter", "custom", "user"):
        # Let the user provide a password and save it to Custom_Passwords.txt
        password = input("Enter your password: ")
        if not password:
            print("No password entered. Aborting.")
            return None
        writePassword("Custom", password)
        print("Password saved to Custom_Passwords.txt")

    else:
        print("Invalid password type.")
        return None

    if password:
        print("Generated password:", password)
    return password


# 1000 passwords generation for confirmation
if __name__ == "__main__":
    # Determine if a positional argument (word file) was provided and collect flags
    wordFile = None
    skipInteractive = False
    for arg in sys.argv[1:]:
        if arg in ("--no-interactive", "-q"):
            skipInteractive = True
        elif not arg.startswith("-") and wordFile is None:
            wordFile = arg

    words = loadWords(wordFile)

    # Generate 1000 passwords for testing
    for _ in range(1000):
        if random.choice(["memorable", "random"]) == "memorable":
            generateMemorable(
                words,
                numWords=random.randint(2, 5),
                caseType=random.choice(["lower", "upper", "title"])
            )
        else:
            generateRandom(
                length=random.randint(20, 30),
                includePunctuation=random.choice([True, False]),
                bannedChars="\"'\\"
            )

    print("1000 passwords generated successfully.")

    # Interactive prompt (unless skipped)
    if skipInteractive:
        print("Skipping interactive prompt (--no-interactive).")
    else:
        try:
            useInteractive = input("Would you like to create a password interactively? (yes/no): ").strip().lower()
        except EOFError:
            useInteractive = "no"

        if useInteractive in ("yes", "y"):
            passwordGenerator(words)

