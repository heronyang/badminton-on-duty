# On-duty Generator for Happy's Badminton Group

## Generate a new on-duty list

1. Save the registered list into a file called `YYYY-MM-DD.txt`.
2. Run `$ python3 main.py YYYY-MM-DD.txt > YYYY-MM-DD-output.txt`.
3. Git add and commit your generated file.

Example (please name the filenames with proper dates):

```
$ python3 main.py 2024-07-07.txt > 2024-07-07-output.txt
$ cat 2024-07-07-output.txt
$ git add . && git commit -m "Add new on-duty list." && git push
```

## Run Locally

```
$ heroku local
```

## Deploy

```
$ git push heroku main
```
