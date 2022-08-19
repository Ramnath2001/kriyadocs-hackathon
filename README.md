# kriyadocs-hackathon

This is my solution for the hackathon conducted by kriyadocs. The problem statement was to create an application that takes a pdf (generated from an application) as input and certifies if
the pdf is valid. To certify that the pdf is valid, it should satisfy a few given rules.

I used python to solve the problem with the help of additional libraries like pymupdf and flask

The entire applications is hosted using pythonanywhere platform.

The app.py is the main file containg the code for the algorithm and the website.

The rest of the python files were used for testing and developing solutions for the given rules.

The following are the basic requirements for running the app.py is:
1. python 3.7 or above must be used
2. pyrebase library must be installed. pip install pyrebase4 is the command for installing this library.
3. pyMuPDF library must be installed. pip install PyMuPDF is the command for installing this library.
4. flask library must be installed. Command for installing - pip install Flask
5. and a few additional libraries must be installed with this command - pip install pymupdf-fonts
  
The application uses firebases for uploading files to the server.

To run the app locally run the app.py files after meeting all the requirements and go to http://127.0.0.1:5000/ to view the app.

This is the link for the website to test my application: http://ramnath2001.pythonanywhere.com/
