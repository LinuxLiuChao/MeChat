from handler import HandlerProcess

from settings import server_host, server_port


def show_menu():
    print(f"\n{'+'* 64}\n")
    print(f"+ login , usage: login <username> <password>")
    print(f"+ logout , usage: logout")
    print(f"+ chat , usage: chat <username> <message>")
    print(f"+ quit , usage: quit")
    print(f"+ help , usage: help")
    print(f"\n{'+'* 64}\n")


if __name__ == "__main__":
    show_menu()
    handler = HandlerProcess(server_host, server_port)
    while True:
        print("Please login first")
        commands = input("Please input command: ")
        if commands == "quit":
            break
        elif commands == "help":
            show_menu()
            continue
        args = commands.split(' ')
        handler.handler(*args)





