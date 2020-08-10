dlib version (19.9.9)
vs 2015 (maybe update 3 ?)
cmake
boost1_66_0
cuda 10.1

python setup.py install
dlib enable cuda
check : cudnn  (cudnn add to system environment variables `PATH`)
check : boost (set boost_root and boost stage, and remove cmake file lines if it still reports error)


### migrate to windows server

- get dlib built package
- remove `dlib setup.py cmdclass`


## Run in development
```
export FLASK_ENV=development
flask run
```

or

You need to tell Waitress about your application, but it doesn’t use FLASK_APP like flask run does. You need to tell it to import and call the application factory to get an application object.
```
pip install waitress
waitress-serve --call 'flaskr:create_app'

```
