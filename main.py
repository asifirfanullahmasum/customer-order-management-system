from dbhelper import DBHelper
from helper import InputHelper


def main():
    db = DBHelper()
    helper = InputHelper()
    while True:
        print(" — — — — — — — — — — — — — — — — MENU — — — — — — — — — — — — — — — — ")
        print()
        print("1) add a customer")
        print("2) add an order")
        print("3) remove an order")
        print("4) ship an order")
        print("5) print pending orders (not shipped yet) with customer information")
        print("6) more options")
        print("7) exit")
        print()
        try:
            choice = int(input())
            if (choice == 1):
                print("Please follow the instructions")
                db.addCustomer(helper.inputCustomer())
                
            elif choice == 2:
                print("Please follow the instructions")
                db.addOrder()
            
            elif choice == 3:
                print("Please follow the instructions")
                db.deleteOrder()
            
            elif choice == 4:
                print("Please follow the instructions")
                db.shipOrder()
            
            elif choice == 5:
                print("Please follow the instructions")
                db.printPendingOrder()
 
            elif choice == 6:
                print('Currently not implemented')

            elif choice == 7:
                break
            else:
                print("Invalid input ! Try again")
        except Exception as e:
            print(e)
            print("Invalid Details ! Try again")



if __name__ == "__main__":
    main()
