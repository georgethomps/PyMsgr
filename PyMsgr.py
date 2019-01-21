# TODO: User's must be signed into iCloud before running!!!
# TODO: all csv column names must be fixed!!!!!!!!!!!
# TODO: mention my assumption is that last names will rarely ever be used, first names will always be used!!!!!!!!!!!!!!!!!!!
# TODO: reduce import statements
# TODO: create function to set current working directory
# TODO: SUPER CONFUSED ON WHAT HAPPENS IF SOMEONE IMPORTS THIS MODULE, WILL RELATIVE PATHS BE PRESERVED???????

# import modules
import re
import csv
import subprocess


# define the PyMsgr class
class PyMsgr:

    # Initialize class and create attributes to store
    # iMessage and SMS contacts
    def __init__(self):

        # create contact attributes
        self.contacts = []
        self.bad_contacts = []

        # create text message attribute
        self.text = ''

        # create text batch attribute
        self.text_batch = []

    # Allow users to export a CSV template
    # for storing contact data in a spreadsheet
    @staticmethod
    def export_contact_template():

        # define column headers
        col_headers = ['first', 'last', 'number']

        # open CSV file to write
        with open('template.csv', 'w') as csv_template:

            # write column headers
            csv_template.write(','.join(col_headers))

        # close file
        csv_template.close()

    # Allow users to export a CSV of bad contacts
    def export_bad_contacts(self):

        # define column headers
        col_headers = ['first', 'last', 'number']

        # open CSV file to write
        with open('template.csv', 'w') as csv_output:

            # create CSV writer
            writer = csv.writer(csv_output, delimiter=',')

            # write column headers
            csv_output.write(','.join(col_headers))

            # write data
            for contact in self.bad_contacts:
                row = [str(values) for values in contact.values()]
                writer.writerow(row)

        # close file
        csv_output.close()

    # Notify user that bad contacts are present and are exported
    def bad_contact_notify(self):

        # check if bad contacts are present
        if len(self.bad_contacts) > 0:

            # export bad contacts and notify user
            self.export_bad_contacts()
            print('\nWARNING: ' + str(len(pymsgr.bad_contacts)) +
                  ' contact(s) were found to be unsuitable for sending'
                  ' messages. Check the "bad_output.csv" for more'
                  ' details.')

    # Allow user to import contacts from a CSV
    def import_contacts_csv(self, csv_path):
        """This function use a CSV file path to
           create a list of dictionaries where each dictionary
           represents an individual contact"""

        # import contacts
        with open(csv_path) as csv_file:
            contacts = list(csv.DictReader(csv_file))
        csv_file.close()

        # store contact data
        self.contacts = contacts

    # TODO: allow user to import contacts from an Excel spreadsheet (POTENTIAL FEATURE)

    # Provide the user a prompt to import contact data from a CSV
    def contacts_prompt(self):

        # ask for CSV path
        csv_path = input('\nEnter the name of your contacts CSV (with ".csv"):\n')

        # import contacts from CSV
        print('\nImporting contacts...\n')
        self.import_contacts_csv(csv_path)
        print('Contacts successfully imported!')

    # Allow user to identify and store bad contacts
    def audit_contacts(self):

        # create variable to remember bad contacts and missing last names
        bad_list = []
        lst_missing = False

        # loop through all contacts
        for contact in self.contacts:

            # store first name, last name and number
            fst, lst, num = contact['first'], contact['last'], contact['number']

            # check if the contact is missing the first name
            # or phone number
            if fst == '' or num == '':

                # append bad contact to bad list
                bad_list.append(contact)

            # check if last name is missing
            if lst == '':
                lst_missing = True

        # loop through bad list and transfer contact from contacts
        # to bad contacts
        for contact in bad_list:
            self.bad_contacts.append(contact)
            self.contacts.remove(contact)

        # notify user if any last names are missing
        if lst_missing:
            print('\nWARNING: Some remaining contacts are missing last names!')

    # Allow user to clear all contacts from PyMsgr
    def delete_contacts(self):

        # Clear contacts, bad contacts, iMessage contacts and SMS contacts
        self.contacts.clear()
        self.bad_contacts.clear()

    # Allow user to delete text batch
    def delete_text_batch(self):

        # delete text batch
        self.text_batch.clear()

    # Allow user to clean contact data to
    # eliminate the potential for applescript errors
    def clean_contacts(self):
        """This function will import a list of contact
           dictionaries and cleanse the data in the following ways:

           1. Strip trailing whitespaces from all data
           2. Properly Capitalize Names
           3. Remove any non-numeric characters from the phone numbers"""

        # notify user contact data is being cleaned
        print('\n\nCleaning contact data...\n')

        # loop through all contacts
        for contact in self.contacts:

            # loop through contact's keys
            for key in contact.keys():

                # 1. strip trailing whitespaces
                contact[key] = contact[key].strip()

                # 2. capitalize names
                if key == 'first' or key == 'last':
                    contact[key] = contact[key].title()

                    # handle last name "Mc" exception
                    if contact[key][:2].lower() == 'mc':
                        contact[key] = contact[key][:2] + contact[key][2:].title()

            # 3. remove any non-numeric characters from the phone numbers
            contact['number'] = re.sub(r'\(|\)|-|\s', '', contact['number'])

        # notify user the contact data was successfully cleaned
        print('Contact data successfully cleaned!')

    # Allow user to print instructions to properly write text messages for recipients
    @staticmethod
    def print_text_instructions():
        """This function provides instructions for the user to format strings
            so they will be compatible with the program. By default, this function
            will only provide the user with instructions, but the "input" argument
            can be used to allow for users to type their message into the program
            if needed."""

        # create instructions prompt
        text_request_msg = \
            ('\n\nPlease enter the message that you would like to text your recipients.\n'
             'Mark the recipient\'s first name with "[first]" and/or her last name with "[last]".\n\n'
             'EXAMPLE: "Hello [first], how are you?" -> "Hello Mark, how are you?"\n\n'
             'WARNING: Do not use tab or enter when typing, only spaces!')

        # display instructions
        print(text_request_msg)

    # Print text message instructions for user and prompt for them to submit a text message
    def text_prompt(self):

        # print instructions
        self.print_text_instructions()

        # prompt use for text message
        print("\ntype your message:")
        self.text = input()

    # Create list of dictionaries that contains phone numbers and the texts to send to each number
    def prepare_texts(self):
        # TODO: test this with one contact (NOT A HIGH PRIORITY, USERS MOST LIKELY WON'T HAVE ONLY ONE RECIPIENT)
        """This function creates a text batch list.
           This object stores the messages to send to the user's recipients as well as
           the number that each message should be sent to."""

        # clear previous text batch
        self.text_batch.clear()

        # loop through contacts to prepare text messages
        for contact in self.contacts:

            # retrieve contact info
            fst, lst, num = contact['first'], contact['last'], contact['number']

            # generate text message
            txt = self.text.replace('[first]', fst).replace('[last]', lst)

            # store text in text batch list
            self.text_batch.append({'number': num, 'text': txt})

    # Ask user if they want to proceed sending texts
    def __txt_warning(self):

        # check if there is a text batch
        if len(self.text_batch) == 0:
            print('\nYou have no messages prepared to send.\nPlease run .prepare_texts() before proceeding.')

        # send general warning to user
        else:
            print('\n\nAre you sure you want to send the following message to your recipients?\n')
            print('MESSAGE: ' + self.text + '\n')
            # TODO: print contacts receiving message (POTENTIAL FEATURE)

            # see if user wants to continue
            choice = input('y/N: ')

            # determine to proceed
            return choice.lower() == 'y'

    # run an applescript to send all texts in a text batch
    def send_messages(self):

        # warn user before proceeding
        proceed = self.__txt_warning()

        # proceed if user selects chooses "y"
        if proceed:

            # open and format iMessage applescript for the subprocess module
            with open('scripts/send_messages.applescript', 'r') as script_file:
                opening_txt = 'osascript<<END\n'
                closing_txt = '\nEND'
                script = opening_txt + script_file.read() + closing_txt
            script_file.close()

            # send all text messages through iMessage using the applescript and text batch
            print('\nSending messages...')
            for recipient in self.text_batch:

                # extract number and text message
                num, txt = recipient['number'], recipient['text']

                # prepare script to run with text and number
                script_ready = script.replace('RNUMBER', num).replace('RMESSAGE', txt)

                # run script and wait for it to complete
                active_script = subprocess.Popen(script_ready, shell=True)
                active_script.communicate()

                # terminate script once complete
                active_script.terminate()

            # notify user process is complete
            print('\nProcess complete')

        # cancel operation if user chooses anything but "y"
        else:
            print('\nCancelling operation...')


# built in menu for users running the library alone
if __name__ == '__main__':

    # initialize PyMsgr
    pymsgr = PyMsgr()

    # welcome user and ask if they want to continue
    print('\nWelcome to PyMsgr! Would you like to continue?\n')
    user_proceed = input('y/N: ').lower() == 'y'

    while user_proceed:

        # ask user to import contacts
        pymsgr.contacts_prompt()

        # audit and clean contacts
        pymsgr.audit_contacts()
        pymsgr.clean_contacts()

        # export bad contacts and notify user
        pymsgr.bad_contact_notify()

        # ask user for text message to send to contacts
        pymsgr.text_prompt()

        # prepare messages
        pymsgr.prepare_texts()

        # send messages to contacts
        pymsgr.send_messages()

        # delete contacts and text batch
        print('\nDeleting contact and text data...')
        pymsgr.delete_contacts()
        pymsgr.delete_text_batch()

        # ask if user wants to send more texts
        print('\nWould you like to send another round of texts?\n')
        user_proceed = input('y/N: ').lower() == 'y'

    # terminate program
    print('\nThanks for using PyMsgr!\n')
    print('Terminating program...\n')
    quit()
