# 🗿 CausalQA API
This API was made so we would be able to keep track of out MTurk data validation pipeline. 

## 💻 The Tech
This API was created using FastAPI. It interfaces with a Redis Cloud instance (as its main database) for its fast key-value storage. 

## 📊 Models
Currently, the only "model" in use is the `Question` model. The `Question` model should be easily created, as almost all of its "columns" are directly mapped to the CSV headers from MTurk. 

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

**Note:** These "models" aren't actual SQL tables (Redis is a key-value store). Rather, they are just used to validate that all of the input parameters are present. 

## 📍 Endpoints
The base URL for the endpoints is tentatively `https://api.justinchang.dev:50000`. 
- **GET** `/api`
  - Hello world test
- **POST** `/api/update_question`
  - Creates or updates a question in the database using the given `Question` model
  - Uses the `Article` as the key
- **GET** `/api/count/:article`
  - Returns the `AssignmentId`, `Q_Drop_Score`, `A_Drop_Score`, and `Total_Possible_Score` for a given `Article`
- **GET** `/api/exist/:article`
  - Returns whether or not a given `Article` exists in the database

## 💡 Feature Requests
If more features are needed, please open an issue on this repository. 