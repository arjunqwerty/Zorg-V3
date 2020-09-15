# Zorg-V3
Under construction
1)wtforms was a pretty good thing, but I'm not sure why we removed it, there should surely be some way to incorporate both wtforms as well as flask-sqlalchemy(even if it is not there, its fine)
2)according to vs-code filter_by has "==", i am not sure if it is the right syntax
for the time being i am removing shivaram's part, we can include it after he sends the online forms version

3)flash, redirect are all part of flask according to the modules imported, please check again if it is actually a part of wtforms only

4) right now the prog works like this:
    4.1)after all registering logging part is done, when a customer presses accident,
    following things happen:
        to orders table a row is created with the same username of the customer, with different usernames of the hospitals, whose so ever is in the same area as that of the customer
        That is, if A, B, C are three hospitals in the same as area as the customer, three rows are created in the order table
    4.2)in dashboard management for every order placed, it showes to them with two links next to it, one to accept, one to decline, when one of them is pressed, it is updated in result 

    WE WILL CHANGE IT NOW LIKE THIS
    a mail is sent from zorg45365@gmail.com to customer's mail id, with subject Zorg-email(something like that), message stating that particular hospital has declined/accepted to save them.

     here mails act in a way similar of whatsapp

    now for the time being, i have made changes only in accident, removed saved and not saved, that is the part that we can temporarily use mails for

    What we need to change:
     1)when the link against each column is pressed by the hospital in the dashboardmnmg, a mail must be sent
     2)change htmls to incorporate gmail id part as well
     3)change all of dashboardmnmg
     4)remove unnecessary tables, eg: result
     5)copy what is there in accident to heartattack, otherailments