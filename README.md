# django-rest-api

A REST api written in Django for people with deadlines

## Technologies used

* [Django](https://www.djangoproject.com/): Django builds better web apps with less code.
* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs

## Installation

* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can
  get python [here](https://www.python.org").
* After doing this, confirm that you have installed virtualenv globally as well. If not, run this:
    ```
         pip install virtualenv
    ```
* Then, Git clone this repo to your PC
    ```
        git clone https://github.com/VitaliiKos/meduzzen-backend-internship_6_2.git
    ```

* #### Dependencies
    1. cd into your the cloned repo as such:
        ```
            cd meduzzen-backend-internship_6_2
        ```
    2. Create and fire up your virtual environment:
        ```
            python -m venv venv
            venv\Scripts\activate
        ```
    3. Install the dependencies needed to run the app:
        ```
            pip install -r requirements.txt
        ```
    4. Make those migrations work
        ```
            python manage.py migrate
        ```

* #### Run It
  Fire up the server using this one simple command:
    ```
        python manage.py runserver
    ```
  You can now access the file api service on your browser by using
    ```
        http://localhost:8000/health_check/
    ```

## Running an application in Docker

#### Build a Docker image

Open a command prompt and navigate to the directory where your Dockerfile and project files are located. Run the
command to build a Docker image:

```
    docker build -t drf_app .
```

Where drf_app is the name of your image, you can specify any name you like.

#### Build a Docker image

After successfully building the image, you can start the Docker container with the command:

```
    docker run -d -p 8000:8000 drf_app
```

Where 8000:8000 is the port mapping, the first number is the port on which your Django application will be available in
the container and the second is the port on which the application will be available on your local machine.

#### Running a Django application

After the Django container is started, the application will be available at http://localhost:8000/. You can go
to http://localhost:8000/health_check in your web browser.

