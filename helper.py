class InputHelper:
    def inputCustomer(self):
        input_value = {}
        customer = {}
        input_value['Company'] = input("Enter Company: ")
        input_value['LastName'] = input("Enter Last Name: ")
        input_value['FirstName'] = input("Enter First Name: ")
        input_value['Email'] = input("Enter E-mail Address: ")
        input_value['JobTitle'] = input("Enter Job Title: ")
        input_value['BusinessPhone'] = input("Enter Business Phone: ")
        input_value['HomePhone'] = input("Enter HomePhone: ")
        input_value['MobilePhone'] = input("Enter MobilePhone: ")
        input_value['Fax'] = input("Enter Fax: ")
        input_value['Address'] = input("Enter Address: ")
        input_value['City'] = input("Enter City: ")
        input_value['State'] = input("Enter State: ")
        input_value['ZIP'] = input("Enter ZIP: ")
        input_value['Country'] = input("Enter Country: ")
        input_value['Web'] = input("Enter Web: ")
        input_value['Notes'] = input("Enter Notes: ")
        input_value['Attachments'] = input("Attachments: ")
        for keys in input_value:
            if input_value[keys] != '':
                customer[keys] = input_value[keys]
        return customer
