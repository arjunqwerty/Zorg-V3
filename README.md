# Zorg-V3
Under construction

The program flows like :
i)Management
Home(index.html) -> Register(remnmg.html) -> Login(lomnmg.html) -> Hospital dashboard(=dashboardmnmg.html) -> Update staff details(updatestaff.html) -> Accept / Decline -> Send mail to customer w.r.mssg
{register - add the info in hospdetails}
{login - compare the info in hospdetails and details entered}
{hospital dashboard - display all the requests, details of staff of the hospital, provision to edit the latter}
{accept / decline - delete the record on such request from order}

ii)Customer
Home(index.html) -> Register(recust.html) -> Login(locust.html) -> Add profile(add_profile.html) / Customer dashboard(=dashboardcust.html) -> Edit profile(editprofile.html) -> Dashboard(dashboardcust.html) -> Accident / Heart attack / Otherailments (request_sent.html) -> Recieve mail from hospital
{register - add info in custdetails}
{login - compare the info in custdetails and details entered}
{addprofile - check if the extra details needed for completion of the custdetails and retrieve details from cust and store in custdetails}
{customer dashboard - display all the customer's info and provision to edit them}
{edit profile - display the previous details and ask for the new ones}
{accident/heartattack/otherailments - check the hospitals in the locality and add the resp. details in order table}
