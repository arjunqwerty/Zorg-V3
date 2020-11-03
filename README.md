# Zorg-V3
**Under testing, applying makeup**

The program flows like :
i)Management
> Home
> Register(remnmg.html)
> Login(lomnmg.html) 
> Hospital dashboard(=dashboardmnmg.html)
> Update staff details(updatestaff.html) -> Accept / Decline -> Send mail to customer w.r.mssg
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

!! IMPORTANT:
Create a branch when you are not sure if your code is correct. you can do that in cli by the following command:

git branch <branch name>
git checkout <branch name>

do all your works in that branch, add files and push and after all that in the website u can create a pull request, this will notify the other person that a fellow peer has done something that he wants you to verify, u can see what new changes he has made, and that way discussions can happer easier

Once done, the pull request is merged to the main master branch by the merge pull request button that will appear after creating the pull request, after clicking that all changes are made to the master branch.

Apparently in an actual office, every person is assigned a code reviewer, this way whatever one does is cross verified
