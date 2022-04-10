# Realsense_test
realsense test

## quick start
1. create Virtual environment
   ```
   $env:PIPENV_VENV_IN_PROJECT = "true" (for Windows)
   export PIPENV_VENV_IN_PROJECT="true" (for Linux)
   ```
2. run shell (require python 3.9)
   ```
   pipenv install
   ```
3. start script
   ```
   pipenv run rec
   pipenv run play
   pipenv run live
   ```