# Osmosis

Osmosis is a automatic employee recruitement portal built using NLTK and flask, used for automatic profile ranking based on resume, and scores of tests of applied job to help recruiters filter profiles. Project does resume analysis for profile ranking. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This project is build upon `Flask framework` in `Python 3.7.5` and `monogodb` for data storage. Any modification would requires basic knowledge of the same.

Follow below installation steps to get this project running on your machine

### Installing

#### 1. Python3 packages
```
pip3 install requirements.txt
python3 -m spacy download en_core_web_sm
python3 -m nltk.downloader words
```

#### 2. Download nltk packages for NLP (natural language processing)
```
      - Open python shell by command `python3` in the terminal
      - >>> import nltk
      - >>> nltk.download()
      - Press option `d`
      - Type `all` and press enter.
```

#### 3. Monogdb
- Follow instructions given on [Mongodb official](https://docs.mongodb.com/manual/administration/install-community/).


## Running the project

To run the project on your local machine follow below steps

#### 1. Download the project repository.
#### 2. Extract the project from Osmosis_v2-master.zip
#### 3. Start monogdb service using ```sudo service mongod start```
#### 4. Navigate to the Osmosis_v2-master folder
#### 5. Install required packages as mentioned above.
#### 6. Run project on local host using ```flask run```.


### Step to execute the project

After successfull installation of the project and setting up the server below steps will help you to execute the project to get the desired output. Project consists of the following apis/projects:

1. Admin Dashboard- http://localhost:5000/admin/dashboard
  - All the added jobs will appear here. Also new jobs can be added from this page.
  
2. Shortlist page
  - Shortlisted or ranked profiles of the employee for a specific job can be viewed by clicking on ```job card``` on the admin dashboard.
  
3. Home page- http://localhost:5000/
  - Starter or main page of the project enables login/signup for the employee.
  
4. Employee dashboard http://localhost:5000/dashboard
  - All the jobs open for application will appear here.
  
5. Profile 
  - Add employee resume and other details here.


## Server and database configuration
```app.py``` is the entry point of the project. To change or add routes, one can easily do it here.
```config.py``` contains all the project configurations.
##### To change security key or your monogdb configuration ```.env``` is the place to do the same.


## Built With

* [Flask](https://flask-doc.readthedocs.io/en/latest/) - The web framework used
* [Creative Tim](https://www.creative-tim.com/) - Material UI kit used

## Contributing

To contribute into it feel free to fork the project add your code and give the pull request for the same.


## Authors

* **Ram Suthar** -  [LinkedIn](https://www.linkedin.com/ram-suthar-234a0a16b)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


