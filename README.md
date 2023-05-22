# CITS5505-Web-Project-Chat-Application
My name is Wendy Wang, my student number is 23454213. And my teammate is Yulin Yu, her student number is 22743739.

First, we built the basic framework of the chat application. We created the home page, login page, registration page and search page. Then initialize Flask and SQLite, add user tables, chat message tables, develop login/registration functions, and support form verification, users can register their own accounts to join in the chat. The real-time chat is developed based on WebSocket. All users can join the public chat room, chat one-on-one privately, and have Q&A with openAI's chatGPT. All chat records will be stored in SQLite, and the historical chat records will be loaded every time a chat is opened. Users can also search for historical chat records based on keywords on the search page.

How to launch from local host, and run your tests and validation?
In the root directory:
1. pip install -r requirements.txt
2. python3 app.py
3. Open in browser:http://localhost:4000
