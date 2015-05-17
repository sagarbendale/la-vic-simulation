from colorama import init, Fore, Back, Style

class Display():
    def __init__(self):
        init()
        self.clear_screen()
        # init()
        # self.clear_screen()
        # self._print_main_title("MAIN TITLE MESSAGE. WELCOME")
        # self._print_title("NORMAL TITLE")
        # self._print_success("Success Message")
        # self._print_error("Error Message")
        # self._print_info("Info Message")
        # self._print_network("Network Message")
        # self._print_conversation("Cashier", "Hello. welcome to la vic")
    
    def _print_success(self, message):
        print(Back.GREEN + Style.BRIGHT  +  Fore.BLACK + " SUCCESS " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _print_info(self, message):
        print(Back.BLUE + Style.NORMAL  +  Fore.WHITE + " INFO " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.NORMAL + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _print_error(self, message):
        print( Back.RED + Style.BRIGHT  +  Fore.WHITE + " ERROR " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _print_network(self, message):
        print( Back.YELLOW + Style.BRIGHT  +  Fore.BLACK + " NETWORK " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _print_title(self, message):
        print(Fore.GREEN + Style.BRIGHT)
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("                 " + str(message))
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def _print_main_title(self, message):
        print(Fore.CYAN + Back.WHITE + Style.BRIGHT)
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print(Back.RESET)
        print( "                        " + str(message).upper()+ "                     ")
        print(Back.WHITE)
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)
        
    def _print_conversation(self, fromPerson, message):
        print(Back.BLACK + Style.NORMAL  +  Fore.CYAN + fromPerson + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def clear_screen(self):
        print("\033c")

d = Display()
