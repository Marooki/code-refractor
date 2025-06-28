#!/usr/bin/env python3

def main():
    cute_character = r"""
     /\_/\
    ( o.o )
     > ^ <
    """
    print("Meet PurrBot!")
    print(cute_character)
    name = input("What's your name? ")
    age = input("How old are you? ")
    country = input("Which country would you like to connect to? ")
    print(f"Scanning for nearby servers in {country} for end-to-end encrypted communication...")
    print("Connection established! Have a secure chat, " + name + "!")

if __name__ == "__main__":
    main()
