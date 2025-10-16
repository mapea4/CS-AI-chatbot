# Ursa The Chatbot

Name: Ursa the AI Chatbot 

Purpose: To make an Artificial Intelligence chatbot that will function as a one stop for Computer Science students at Morgan. 

Features:  

Take user input based off the services we have made. (E.X- “Course help”, or “Looking for forms?”) and direct them to the link or webpage we made with that data. 
A calendar of general events most CS students would need to know about.(Depending on time) 
A feature where you would look up what class is being offered in the current semester and be directed to the professors and TA’s associated with that class. 
Have a major curriculum link that shows what classes the students should be taking based on their classification. 
Have a link that displays the classroom of each course being offered in the semester.  
Have a link that will display all the different forms that may be helpful to CS students. (Maximum Credit Form, Prerequisites override form, etc.) 
 

Front End 

-Make the front end look similar to chatGPT but morgan themed 

Back End 

We’re dealing with the data that we input from morgan’s website that gives info that CS students need. (Use a text file maybe) 
The AI will see what the user types and use the info in the text file to give the best answer. 
Use RAG to grab updated info from other website  
Need a database for user login(MySQL and PHP) 
Need to make sure our AI is trained enough to answer questions correctly for security(Using ChatGPT’s open AI) 
Backend Template 

1. Data Management (Knowledge Base) 

Owner: Bryan 
What to do: 
Collect info from Morgan’s CS website (course catalog, professors, forms, events, curriculum). 
Organize all data into one structured text file (knowledge_base.txt) with sections (like [COURSES], [PROFESSORS], [FORMS]). 
Write a simple data loader that reads this file into Python (dictionary format). 
Later: prepare scripts to update this file using RAG (Retrieval-Augmented Generation). 
 

2. Query Handling + AI Logic 

Owner: Marquise  
What to do: 
Build query_handler.py that searches inside knowledge_base.txt. 
Add fuzzy matching (so “data structures” = “CSCI 241”). 
Connect chatbot.py to OpenAI API so it can rewrite answers more naturally. 
Handle intents: 
“course help” → search [COURSES] 
“forms” → search [FORMS] 
“curriculum” → [CURRICULUM GUIDE] 
By Oct 16: be able to type a question in terminal → get an answer from the text file. 
 

3. Web Server + API 

Owner: Matan
What to do: 
Set up Flask app (app.py) with route /api/chat. 
Connect Flask route to chatbot.py → return answers as JSON. 
Build basic error handling & logs. 
Set up database connection (MySQL + PHPMyAdmin). 
By Oct 16: have working API where Postman/cURL can send a message and get a chatbot response. 
 

4. Database + Authentication 

Owner: Dawaun 
What to do: 
Create MySQL schema for users (id, username, password, saved chats). 
Write backend code (auth.py) to handle login/signup. 
Secure passwords (hashing with bcrypt). 
Connect Flask routes for login & register. 
By Oct 16: user can register/login with dummy data. 
 

Timeline 

10/2: Start producing the backend  
10/9: Continue working on Backend while also making the front end 
10/15: Finishing touches and submitting report 
