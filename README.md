# Scavenger
Project for SBHacks
##Inspiration
Oftentimes, we noticed that people subscribe to tons of websites but never actually bother to read their promotion emails. Mostly, they are swamped and bombarded by those emails and only ended it up marking them as spams. To solve this problem, we built Scavenger, a web app that saves the trouble for the users and gives them instant access to the most valuable contents from the promotion emails they have subscribed to.

##What it does
Scavenger first collects promotion emails from a user's email account. Then it analyzes them using IBM-Watson Bluemix to throw away garbage contents. Eventually it displays the most valuable information such as "discounts" or "new products" in a single cascade of images, sorted according to product brands. It also preserves the link on the images so that the users could click on to directly to visit the product page. It saves the user the time and trouble of going through all of their subscriptions, and allows them to view everything in a single scroll.

In order to test our ideas in the hackathon, the prototype we made only focuses on newsletters from fashion brands websites, such as Nike, Adidas, Timberland, A&F, etc.

##How we built it
For the front-end, we used html5 and css3 to build the graphics and buttons. We also managed to present all the images in an elegant responsive photo-grid layout by css3.

For the back end, there are two parts: the server back end and the email parsing program. We used node.js and express to build the website, and connected to MongoLab's MongoDB for database, nothing fancy here. For the email parsing, as now for the demo we only need to test one single account, we connected to the email account specifically for receiving promotional emails, and retrieve all the unread messages every five minutes. Once a message is received, the program with parse it and upload the proper objects to the MongoDB server.

##Challenges we ran into
How to parse email At first we thought the format of an email should be simple and we should be able to get the body of the email easily. However, we found that within the python email package, there was no "body" or "content" key for an email message object. We solved this problem by knowing that the emails we are dealing with are all multi-parts and we iterated through the payloads to further process the contents.

How to determine the essential emails of the email Since every email has different formats and styles, it is hard to draw a line between meaningless pictures and the important ones. One mentor suggested that we use IBM watson's image recognition, to collect tags for each image and then filter the images by the tags they have. This is indeed an elegant way to solve the problem.

##Accomplishments that we're proud of
One accomplishment must be that we successfully decoded the mysterious format of emails and extracted all the information we need. Besides, we figured out how to determine "good" and "bad" images with the help of IBM's image recognition API.

In addition, by using only css3, we were able to present all the photos in a simple and responsive photo-grid. The size and number of columns will change according to the size of the display, and no matter how big or small or weirdly shaped the images are, the width of the columns will always be equally divided according the window size.

##What we learned
In building this web app that integrates multiple languages and API's, we have learned:

Better control over html5, css3
How to use mongodb, IBM-Watson Bluemix, beautiful soup, and some useful API's
Time management and prioritization

##What's next for Scavenger
Right now, Scavenger could only work with emails users received from various websites they have signed up over the years. Our next step would be to build a data base of popular subscriptions, and instead of subscribing to websites on their own, users could simply register at our platform and browse the refined version of all the newsletter at their will. In other words, one single sign-on and off you go!

P.S.: when visiting the first link below, please refresh a few times if the images don't show up immediately or are incomplete.
