from MeChatClient.handler import HandlerProcess


def show_menu():
    print(f"\n{'+'* 64}\n")
    print(f"+ login , usage: login <username> <password>")
    print(f"+ logout , usage: logout")
    print(f"+ chat , usage: chat <username>")
    print(f"+ quit , usage: quit")
    print(f"\n{'+'* 64}\n")


if __name__ == "__main__":
    while True:
        show_menu()
        handler = HandlerProcess()
        print("Please login first")
        commands = input("Please input command: ")
        if " " in commands:
            args = commands.split(' ', 1)
            handler.handler(*args)
        else:
            if commands == "quit":
                break



