# TypeChat

## Build Setup

```bash
# install dependencies
$ pip install -r requirements.txt
$ cd app
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

# run api server
$ uvicorn main:app --reload

# generate static project
$ export BASE_URL=/
$ npm run generate
```

For detailed explanation on how things work, check out [Nuxt.js docs](https://nuxtjs.org).
For API documentation, run the server then go to http://localhost:8000/docs