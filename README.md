# PyMsgr

**Project Description**

PyMsgr is a Python module/script that allows OS X users to send mass text messages through iMessage. This program allows its
users to import contacts from a CSV, submit a text message template to indicate where PyMsgr must places names in the messages,
and send all text messages through iMessage. PyMsgr can be run as a standalone script or developers can use it as a module to 
utilize such features in their code.

&nbsp;

**File Guide**

Script: `PyMsgr.py`

Example Contacts CSV: `contacts.csv`

&nbsp;

**Additional Comments * Concerns**

This program will only work in OS X; this will not work for Windows or Linux users. This program was built under the 
assumption that its users will rarely ever use last names when sending texts. As a result, when the program scans for contacts
with insufficient data, contacts without last names will not be removed. 

In regards to sending SMS messages, the program seemed to send SMS text through iMessage when ran on my computer. However,
my laptop has issues sending SMS messages through iMessages, so they were no longer delivered. Although it's unknown to me
whether this feature works, it's fortunate that most people use the iMessage platform.

As of now, I did not write any documentation to use PyMsgr as a module. If this project is subject to interest I will write
proper documentation to use PyMsgr's methods.

&nbsp;

**Running the PyMsgr as a standalone application**

1. Make sure your contacts CSV, PyMsgr.py script, and Scripts folder all placed in the same folder. Make sure your contacts
   CSV precisely matches the structure on the 'contacts.CSV' in this repository!

2. Open your local terminal and cd into the folder where you placed the files from step 1.

3. Run "python3 PyMsgr.py" or "python PyMsgr.py" (depending on your OS). If neither command works, you most likely need to 
   install Python 3 on your computer
   
3. Enter the information requested by the program and your texts will be successfully sent!
