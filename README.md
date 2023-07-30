# GraduationProject_Backend
## Sahelna | A Governmental Website for Both the Citizen and the Government <br>
Welcome to Sahelna, a comprehensive platform designed to facilitate communication and improve government services for citizens. Our platform provides citizens with information on the specific paperwork required to perform various governmental services and offers centralized resources for exploring existing governmental applications. Additionally, we provide a space for citizens to share their experiences and opinions through reviews of governmental services. Our Sentiment Analysis model is leveraged to facilitate a deeper understanding of citizen sentiment towards the services provided.
<br>

### Frontend Repository [Click Here](https://github.com/Asmaa-Refat/FrontEnd-GraduationProject)
### Backend Repository
The backend of our project is built using Django and contains the Sentiment Analysis model. This repository contains all the code for the server-side logic, including database models, views, and URLs.
<br> <br>
### **Sentiment Analysis Model** |  We tried so many Machine Learning algorithms like 
- **SVM accuracy 85.5%**
- multinomialNB accuracy 80.91%
- Random Forest accuracy 81.83 %
- Gradient Boosting accuracy 77.5 %
- Neural Network accuracy 81.64 %
- Deep Neural Network  accuracy 81.95 %
- CNN accuracy 78.13 %
- RNN accuracy 79.15 %
- LSTM accuracy 83.38 %
- GRU accuracy 83.05 %

### To run the backend, follow the instructions below: <br>
- Clone this repository to your local machine.
- Navigate to the root directory of the project in your terminal.
- Create a virtual environment and activate it.
- Run this commands to install all the dependencies.
  - ```
    pip3 install django
    pip3 install djangorestframework
    python -m pip install Pillow
    pip3 install emoji --upgrade 
    pip3 install PyArabic
    pip3 install nltk
    pip3 install -U scikit-learn
    pip3 install pandas
    pip3 install django-cors-headers
    ```
- Run python manage.py makemigrations    
- Run python manage.py migrate to create the database tables.
- Run python manage.py runserver to start the development server.
- Navigate to http://localhost:8000/ in your web browser to view the backend.
