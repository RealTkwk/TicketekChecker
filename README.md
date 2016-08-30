# TicketekChecker

This is a really small 10 minute project to scrape Ticketek's news site (www.ticketek.com.ar) for new additions when the page is empty. When something new appears, the script stops running and notifies any recipients. It was made to avoid having to subscribe as the newsletter is too cumbersome.

Right now it has a very specific usage as this won't work when there are previous events. In the future I'm planning to add some more features like making the script notify the user when something new comes up without stopping and just sending the newer shows.

In ored to use it (with Python3) you have to generate a file called `settings.cfg` which contains the next info in that order:

1. Gmail account to send the notification
2. Account password
3. Email to send the notification
4. Tickete url to check
5. Frequency to check
