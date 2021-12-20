### Pre Requirements

* ffmpeg (required by librosa to load mp3)
* nodejs (frontend)
* MongoDB

### Environment Setup

Inside `backend/.env`:

Edit the default MONGO_URI to your mongodb connection key

```env
MONGO_URI=mongodb://localhost:27017/?readPreference=primary&serverSelectionTimeoutMS=2000&appname=MongoDB%20Compass&directConnection=true&ssl=false
FLASK_ENV=development
```

**Backend**

1. Create conda env (optional)

`conda create --name kishikan python=3.8`

`conda activate kishikan`

2. Install python dependencies (in `backend`)

Please navigate to `backend` folder, then

`pip install -r requirements.txt`

3. Configure flask (in `backend`)

`export FLASK_APP=app`

start the flask using `flask run`

**Frontend**

Please navigate to `frontend` folder, then

`yarn install ` to install dependencies

`yarn start` to open client

### Important Folders Structure

```
.github
-- postman collection for API testing
backend
-- app/: all code to implement RESTful Flask Server
-- kishikan/: audio fingerprinting module
-- nazo/: query by humming module
frontend: react frontend code in typescript
```

### Demo

Please open `backend/audio_fingerprinting.ipynb` for audio fingerprinting, and `backend/query_by_singing.ipynb` for query by humming.

### Experiments

If you want to perform experiments, please download the datasets and place them into `datasets/`:

GTZAN and it's query: https://www.music-ir.org/mirex/wiki/2021:Audio_Fingerprinting

QBSH midi and query: https://www.music-ir.org/mirex/wiki/2021:Query_by_Singing/Humming

Benchmark usage can be found inside jupyter notebooks in `backend/`

