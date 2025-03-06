<a name="Pet API Test Automation Project"><h2>Pet API Test Automation Project</h2></a>

This project is an automation testing suite for the Pet API. The tests verify various API endpoints, including creating, editing, and deleting pets, among other functionalities.
<a target="_blank" href="https://petstore.swagger.io/#/pet">Link</a> to API handles in swagger.

\
Install the dependencies with the following command:
```
pip install -r requirements.txt
```

\
Run all tests with:
```
pytest --alluredir=allure-results
```

\
To view the Allure report:
```
allure serve allure-results
```



