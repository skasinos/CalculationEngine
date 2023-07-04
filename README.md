# CalculationEngine

## Set-up Instructions

1. Clone repository:
    ```latex
    cd Desktop && git clone git@github.com:skasinos/CalculationEngine.git && cd CalculationEngine
    ```
2. Setup `pyenv` and install `poetry` dependencies:
    ```latex
    pyenv local 3.10.0 && poetry env use 3.10.0 && poetry install
    ```

3. Open the project in an IDE e.g. [PyCharm](https://www.jetbrains.com/pycharm/). The interpreter should be picked up automatically.

4. Enter directory where `manage.py` is located:
      ```latex
    cd calculation_engine
      ```

5. Start the development server:

      ```latex
    python manage.py runserver
      ```



  
## Usage

### API

- A user may send a `POST` request (e.g. via [Postman](https://www.postman.com/)) to [http://localhost:8000/emissions/calculate-emissions/](http://localhost:8000/emissions/calculate-emissions/) providing the `activity_data` and `emission_factors` csv files as form data. Upon a successful request, emissions will be calculated and stored in the database. It is noted that the database [db.sqlite3](https://www.swagger.io) already contains the emissions associated with the three provided activity data files. Notably, other `activity_data` input files may be used, should it be of interest.
    
  - A specific scope or category may be fetched via e.g. http://localhost:8000/emissions/emissions/?scope=2 or http://localhost:8000/emissions/emissions/?category=6

- A user may retrieve emissions via a `GET` request to [http://localhost:8000/emissions/emissions/](http://localhost:8000/emissions/emissions/). A successful request should return e.g.:
    ```latex
    {
        "emissions": [
            {
                "id": 1,
                "co2e": 1515.0,
                "scope": 3,
                "category": 1,
                "activity": "PURCHASED GOODS AND SERVICES",
                "unit": "GBP"
            },
            ...
        ],
        "total_emissions": 145524.95
    }
    ```
- A user may update an emission via a `PUT` request to [http://localhost:8000/emissions/emissions/pk/](http://localhost:8000/emissions/emissions/pk/), where `pk` is to be replaced with the primary key of the `Emission` object of interest.
- A user may delete an emission via a `DELETE` request to [http://localhost:8000/emissions/emissions/pk/](http://localhost:8000/emissions/emissions/pk/), where `pk` is to be replaced with the primary key of the `Emission` object in question.

### UI

- Emissions may be displayed on the UI by navigating to [http://localhost:8000/emissions/emissions/](http://localhost:8000/emissions/emissions/)
- At the very end of the list `Total emissions` are displayed, representing the total emissions sum.
- Emissions may be sorted by CO2e in descending order by pressing the `Sort by CO2e` button. 
- Emissions may be grouped by activity and aggregated together by pressing the `Group by Activity` button.
- Emissions may be filtered by scope and category through the `All Scopes` and `All Categories` dropdowns.


## Limitations & Improvements
- Currently, for every `activity_data` csv file, an `emission_factors` file is required. A potential improvement is to store `EmissionFactors` in the database. A `POST` request should then have an optional `emission_factors` file input. In the absence of this file, `emission_factors` are fetched from the database and used in the calculation.
- To prevent duplicated objects with the same values being created in the database `unique_together` may be used in conjunction with the date provided in the `activity_data`.
- Input files other than `.csv` may be supported.
- A test database needs to be configured and parametrized unit tests should be written to check endpoints as well as the calculation of emissions.
- In an analogous way to how [Money](https://py-moneyed.readthedocs.io/en/latest/usage.html) objects can be handled, the amounts and units of attributes could be better handled / represented together.
- API documentation may be setup via [Swagger](https://www.swagger.io)
- Unit conversion was only implemented for miles and kilometres. In future, this should be dealt through a more comprehensive approach allowing further conversions.
- In the html, scope and category options were hardcoded by inspecting the data. These need to be dynamically provided from the database.

## Developer notes

- Following model changes, make migrations and migrate:

    ```latex
    python manage.py makemigrations && python manage.py migrate
    ```

- A [shell_plus](https://django-extensions.readthedocs.io/en/latest/shell_plus.html) may be started via the following command, defined in `package.json`, which may be extended with other commands:
    ```latex
    yarn shell
    ```

- Additional apps should be created at the same level as the `emissions` app.
