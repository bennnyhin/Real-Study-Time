# Real-Times
### Time management and tracking [web application](https://real-times.herokuapp.com/) with machine learning features

### Pitch
Most existing time management apps simply track your time usage on a task; RealTime tracks how long you expect to spend on a task and compares it to the actual time. Our users have complete control over their data; all statistics are available on a “stats for nerds” page, which provides intuitive statistics and graphs that can be tuned to a user’s liking in order to visualize effectiveness. Through this data, students will be able to better manage their time because they can quantify how long their work will take them in comparison to their initial expectations. We also facilitate the use of this service by using a simple UI that will appeal to everybody. An advanced regression-based machine learning algorithm also predicts the timeline of their project. The result is a user-oriented app that promotes strong time management and efficiency.

### Features
Users are greeted with our landing page which prompts them to log in or create an account. We use secure encrypted databases to store password hashes. Next, they are directed to our main page, where a table shows tracking history as well as a sidebar to start a new session. Users input the task name, and the expected time it will take, then press the START button. The user is then redirected to a page where a timer then appears, counting up towards their predicted time; it is now safe to minimize or close the webpage. When the user is finished, they simply click “complete” and their time is logged, and their personal predictive model is trained with the new data. The user also has access to a statistics page from the main site, where they can view statistics such as average expected time, average actual time, difference, average minutes over expected, and even a graph with many options to tune as the user pleases. We are proud of our intuitive model and data visualization.

Here is an image of our statistics page
![stats page](https://drive.google.com/uc?export=download&id=1Nz1hBLbr-JRydzRi4qn5JyFHx5XtGgS_)

Image of our login page
![login page](https://drive.google.com/uc?export=download&id=1ZF7V_XPTUQaeM9M2i3ALLHVLRwKNbNq1) 

### Getting Started
Simply go to [our website](https://real-times.herokuapp.com/) and follow along. If you do not wish to create an account, we have an example user: 

Username: f
Password: f

To run locally, execute the following commands in the terminal:

* `git clone https://github.com/bennnyhin/real-times`
* `pip3 install -r requirements.txt` 
* `flask run`

Finally, navigate to your browser and type in the following url: `http://127.0.0.1:5000/`

### Made during hackMIT (September 18-20, 2020) by:
* **Benjamin Ng** - [bennnyhin](https://github.com/bennnyhin)
* **Michael Xu** - [themicklepickle](https://github.com/themicklepickle)
* **Arnav Kumar** - [arnavcs](https://github.com/arnavcs)
* **Stanley Zheng** - [Stanley-Zheng](https://github.com/Stanley-Zheng)
