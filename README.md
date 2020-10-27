# TypeChat
Is a forum built around the idea of typing based authentication. 
If you don't have a password to forget, then you don't need an email for password resets. 
If you don't need an email then there's no need to sign up. Just pick a username and start typing!
## Dev Setup

```bash
# install dependencies
pip install -r requirements.txt
cd app
npm install

# serve with hot reload at localhost:3000
npm run dev

# run api server
uvicorn main:app --reload
```

# Build docker container
```
export BROWSER_BASE_URL=/
npm run generate
docker build -t typechat .
# Create environmental variables and pass them to the container
docker run -d --name NAME -e API_KEY -e API_SECRET -e SECRET_KEY -p 80:80 typechat
```

For detailed explanation on how the UI things work, check out [Nuxt.js docs](https://nuxtjs.org).

For API documentation, run the server then go to http://localhost:8000/docs