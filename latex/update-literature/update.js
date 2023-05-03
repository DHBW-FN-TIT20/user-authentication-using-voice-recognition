const fs = require('fs');
const path = require('path');
const axios = require('axios');

const url = 'https://api.zotero.org/groups/4917315/items/?format=bibtex&limit=10000';

// ../literatur/literatur.bib
const filePath = path.join(__dirname, '..', 'literatur', 'literatur.bib');

axios.get(url)
    .then((response) => {
        fs.writeFileSync(filePath, response.data);
    })
    .catch((error) => {
        console.log(error);
    });
