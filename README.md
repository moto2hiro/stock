# README #
  
## Backend Setup (Python)  
  
  * Environment Setup (Just for the first time)
    * Download Anaconda3
    * Open Anaconda Terminal
    * Create Environment (Windows) May take 30min  
``conda env create --file c:\path\to\repo\stock\stock_env.yml -n stock_env``  
    * Create Environment (Mac) May take 30min  
``conda env create --file /path/to/repo/stock\stock_env_mac.yml -n stock_env``  
  * Start Development
    * Open Anaconda Terminal
    * Activate Environment  
``conda activate stock_env``
    * Change Directory to src-backend  
``cd c:\path\to\repo\stock\src-backend``
    * Run Flask  
``python app.py``
  * Environment Update to *.yml
    * Open Anaconda Terminal
    * Activate Environment  
``conda activate stock_env``
    * Install Library from Anaconda
    * Update Environment to *.yml (Windows)  
``conda env export --name stock_env > stock_env.yml``
    * Update Environment to *.yml (Mac)  
``conda env export --name stock_env > stock_env_mac.yml``  
    * Git commit and push update file
  * Environment Update from *.yml
    * Git pull from git repo.
    * Open Anaconda Terminal
    * Activate Environment  
``conda activate stock_env``
    * Update Environment from *.yml (Windows)  
``conda env update --name stock_env --file c:\path\to\repo\stock\stock_env.yml`` 
    * Update Environment from *.yml (Mac)  
``conda env update --name stock_env --file /path/to/repo/stock/stock_env_mac.yml``  
  * Unit Test
    * Open Anaconda Terminal  
    * Activate Environment  
``conda activate stock_env``  
    * Change Directory to src-backend  
``cd c:\path\to\repo\stock\src-backend``  
    * Run All Unit Tests  
``python -m unittest -v``  
    * Run Single File Unit Test  
``python -m unittest -v test.test_app_utils.test_number_utils``  
  
  
## Frontend Setup (ReactJs)  
  
  * Environment Setup (Just for the first time)  
    * Download Node Js
    * Change Directory  
``cd c:\path\to\repo\stock\src-frontend``  
    * Get Packages  
``npm install``  
  * Start Development  
    * Change Directory  
``cd c:\path\to\repo\stock\src-frontend``  
    * Start (Windows)  
``npm start``  
    * Start (Mac)  
``unset HOST``  
``npm start``  


## IDE Setup (VSCode)  
  
  * Extensions  
    * ES7 React/Redux/GraphQL/React-Native snippets  
    * JavaScript (ES6) code snippets  
    * Prettier - Code formatter  
    * Python  
    * sort-imports  
  * settings.json  

```json
{  
  "editor.formatOnSave": true,  
  "python.linting.pylintArgs": ["--load-plugins", "pylint_flask"],
  "python.formatting.autopep8Args": ["--indent-size=2", "--max-line-length=200"],
  "emmet.includeLanguages": {
    "javascript": "javascriptreact"
  },
  "prettier.jsxSingleQuote": true,
  "prettier.singleQuote": true,
  "prettier.printWidth": 120,
  "[javascript]": {
    "editor.tabSize": 2
  },
  "[json]": {
    "editor.tabSize": 2
  },
  "editor.insertSpaces": true,
}
```