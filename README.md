
#### Simple banking system

Description
This is the basic banking system. It includes the opportunity to deposit money into an account, make transfers and close an account if necessary.


Full menu looks like this:
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit


If the user asks for Balance, system should read the balance of the account from the database and output it into the console.
Add income item should allow users to deposit money to the account.
Do transfer item should allow transferring money to another account. It should handle the following errors:
*	If the user tries to transfer more money than he/she has, output: "Not enough money!"
*	If the user tries to transfer money to the same account, output the following message: “You can't transfer money to the same account!”
*	If the receiver's card number doesn’t pass the Luhn algorithm, program should output: “Probably you made mistake in the card number. Please try again!”
*	If the receiver's card number doesn’t exist, program should output: “Such a card does not exist.”
*	If there is no error, it asks the user how much money they want to transfer and make the transaction.
If the user chooses the Close account item, the account is deleted from the database.


The system also generates the CARD NUMBER, PIN and checks validity of the card number by the Luhn algorithm. 

A PIN code is a sequence of any 4 digits. PIN is generated in a range from 0000 to 9999.
CARD NUMBER starts with 400000 IIN number. The seventh digit to the second-to-last digit is the customer account number (randomly generated). The very last digit of a credit card is the check digit or checksum. It is used to validate the credit card number using the Luhn algorithm.




