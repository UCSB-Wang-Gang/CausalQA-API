# 🗿 CausalQAPI
This API was made so we would be able to keep track of out MTurk data validation pipeline. The API is currently hosted with the base URL being `https://api.justinchang.dev:50000`. 

## 💻 The Tech
This API was created using FastAPI. It interfaces with a Redis Cloud instance (as its main database) for its fast key-value storage. 

## 🛠 Setup
To setup the API for local development you will need to install its dependencies. To do so, run the command:
```
pip install -r requirements.txt
```

Afterwords, you must configure the Redis integration by configuring the following environment variables:
```
export REDIS_HOST=REDIS_HOST_URL_HERE
export REDIS_PORT=REDIS_PORT_HERE
export REDIS_USERNAME=YOUR_USERNAME_HERE
export REDIS_PASSWORD=YOUR_PASSWORD_HERE
```

(Optional) To run the API over `HTTPS`, configure the following environment variables: 
```
export SSL_KEY=PATH_TO_SSL_KEY
export SSL_CERT=PATH_TO_SSL_CERT
```

Also make sure that the following line is uncommented in `main.py`:
```py
ssl_keyfile=os.environ.get('SSL_KEY'), ssl_certfile=os.environ.get('SSL_CERT'),
```

**Note**: If running into an error similar to `httptools.parser.parser.HttpParser.feed_data httptools.parser.errors.HttpParserInvalidMethodError: invalid HTTP method`, verify that your environment variables are being used as source. 

## 📊 Models
Currently, the only "model" in use is the `Question` model. The `Question` model should be easily created, as almost all of its "columns" are directly mapped to the CSV headers from MTurk. The "models" aren't actual SQL tables (Redis is a key-value store). Rather, they are just used to validate that all of the input parameters are present. 

### Question
  - HITId `str`
  - AssignmentId `str`
  - WorkerId `str`
  - Question `str`
  - Answer `str`
  - Article `str`
  - Fact `str`
  - Q_Drop_Score `str`
  - A_Drop_Score `str`
  - Total_Possible_Score `str`

## 📍 Endpoints
- **GET** `/api`
  - Hello world test
- **POST** `/api/update_question`
  - Creates or updates a question in the database using the given `Question` model
  - Strips the `Article` so the URL components are removed and uses the result and `AssignmentId` as the key
  - Appends or updates the `Question` with the given `Article` and `AssignmentId`
- **GET** `/api/scores/:article_name`
  - Returns the `Q_Drop_Score`, `A_Drop_Score`, and `Total_Possible_Score` for all questions in `:article_name`
- **GET** `/api/scores/:article_name/:assignment_id`
  - Returns the `Q_Drop_Score`, `A_Drop_Score`, and `Total_Possible_Score` for the questions with `:article_name` an `:assignment_id`
- **GET** `/api/count/:article_name`
  - Returns the number of questions with `:article_name`

## 💡 Feature Requests
If more features are needed, please open an issue on this repository. 