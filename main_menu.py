def mainMenu():
    print()
    print("Welcome to Sonara " + displayName + "!")
    print()
    print("What would you like to do?")
    print()
    print("0 - Search for an artist")
    print("1 - Display current playing song")
    userChoice = input(str("Enter your selection here: "))

    if userChoice == "0":
        getArtist()
    
    if userChoice == "1":
        print()
        print()
        print(getCurrentSong())
        print()
        print("Would you like to see the lyrics?")
        print("0 - Yes, display lyrics!")
        print("1 - No, take me back to main menu...")
        userChoice = input(str("Enter your selection here: "))

        if userChoice == "0":
            getLyrics()
            mainMenu()
        else:
            mainMenu()