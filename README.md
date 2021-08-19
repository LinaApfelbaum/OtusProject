# OtusProject

Testing of Mail.ru mail client web interface

### Setup mail.ru account
- Switch account language to English

- Create app passwords for smtp\pop3 interaction
mail.ru / Settings / All settings / Security / Passwords for external applications

Install packages

```pip install -r requirements.txt```

Clean allure results

```./clean.sh```
   
Run tests (local)

```
pytest \
--executor local \ 
--login "main_account@mail.ru" \
--password "main_account_password" \
--app_password "app password" \
--sender_email sender@mail.ru \
--sender_app_password "sender password" \
tests
 ```

Run tests (Selenoid)

```pytest --executor selenoid_host:4444 --numprocesses 2 tests ```

Lint code

```pylint page_objects/ tests/ utils```
