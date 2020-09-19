# Zorg-V3
Under construction
"Arjun"
1. I have changed the class "custdetails" to "CustomerDet", class "order" to "Order", class "pastorder" to "PastOrder", class "result" to "Result" since the program is getting confused between the table 'custdetails' and class 'custdetails'.....
2. Added empty string and 0 as value in registering since the adding to the table needs all the coloumn to be added. Hence we need to update in addprofile and edit profile and not add.
3. Added register & login htmls, the static folder pics, etc.

The program flows like :
I(Management)
Home(index.html) -> Register(remnmg.html) -> Login(lomnmg.html) -> Hospital dashboard(=dashboardmnmg.html) -> Update staff details(updatestaff.html) -> Accept / Decline -> Send mail to customer w.r.mssg
{register - add the info in hospdetails}
{login - compare the info in hospdetails and details entered}
{hospital dashboard - display all the requests, details of staff of the hospital, provision to edit the latter}
{accept / decline - delete the record on such request from order}

II(Customer)
Home(index.html) -> Register(recust.html) -> Login(locust.html) -> Add profile(add_profile.html) / Customer dashboard(=dashboardcust.html) -> Edit profile(editprofile.html) -> Dashboard(dashboardcust.html) -> Accident / Heart attack / Otherailments (request_sent.html) -> Recieve mail from hospital
{register - add info in custdetails}
{login - compare the info in custdetails and details entered}
{addprofile - check if the extra details needed for completion of the custdetails and retrieve details from cust and store in custdetails}
{customer dashboard - display all the customer's info and provision to edit them}
{edit profile - display the previous details and ask for the new ones}
{accident/heartattack/otherailments - check the hospitals in the locality and add the resp. details in order table}


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
