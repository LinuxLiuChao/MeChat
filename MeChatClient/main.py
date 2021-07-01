from handler import HandlerProcess


def show_menu():
    print(f"\n{'+'* 64}\n")
    print(f"+ login , usage: login <username> <password>")
    print(f"+ logout , usage: logout")
    print(f"+ chat , usage: chat <username> <message>")
    print(f"+ quit , usage: quit")
    print(f"\n{'+'* 64}\n")


if __name__ == "__main__":
    url = "ws://localhost:9888/chat"
    while True:
        show_menu()
        handler = HandlerProcess(url)
        print("Please login first")
        commands = input("Please input command: ")
        if commands == "quit":
            break
        args = commands.split(' ')
        handler.handler(*args)





