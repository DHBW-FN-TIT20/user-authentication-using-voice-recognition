# Client Demosystem

## Setup client
### Install node modules
```bash
npm install
```

### Setup server connection parameters
The server connection parameters are defined in [src/config.json](src/config.json).
```JSON
{
    "SERVER_URL": "127.0.0.1",
    "SERVER_PORT": 5500
}
```

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.
