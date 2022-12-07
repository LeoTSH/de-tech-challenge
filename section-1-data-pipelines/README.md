Data Generation:
* 100 rows of mock data were generated.
* 10% of the data have empty names.
* 20% of the data have errant emails (Empty or format issues)

Websites Used:
* https://www.random-name-generator.com/: To generate fake names. Mix of Chinese Malay and Indian names
* https://www.mockaroo.com/: To generate fake emails
* https://www.coderstool.com/fake-test-identity-data: To generate mobile numbers
* https://onlinerandomtools.com/generate-random-date: To generate birthdays

Mock Dataset Columns:
* name
* dob
* mobile
* email

Cleaned Dataset Columns:
* name
* age
* above_18
* dob
* mobile
* email
* first_name
* last_name
* member_id

Usage:
* Navigate to the section-1-data-pipelines folder
    * `de-tech-challenge\section-1-data-pipelines`
    * Run `python ./src/main.py` to generate the final dataets
    * Run `pytest ./tests/unit_tests.py --cov-report html:./tests/results --cov=src` to generate the coverage and pytest results

Assumptions:
* Christian names are not used
* For Chinese names: Surname (Last name) + Given name
    * For Example: Tan Ah Kow Andy
        * Surname: Tan, Given name: Ah Kow
* For Malay & Indian names: As they do not have familiy names, I've opted to denote/separate based on the patronymic terms (Bin, Binte, d/o, s/o)
    * For example: Indra Venkiteswaran d/o P. Anand
        * Surname: P. Anand, Given name: Indra Venkiteswaran
    * For example: Mohammad Rohan Bin Mohamamad Andika
        * Surname: Bin Mohamamad Andika, Given name: Mohammad Rohan
* Formats and combinations of names are not exhaustive, an analysis of production data will be required to have a better picture
