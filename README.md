# Django Tests

## Description

In this exercise, you will write unit tests to see if your code from the exercise on [Django Sessions](https://github.com/dci-python-course/Python-basics-django-sessions) does what is expected to do and there is no unexpected behavior.

## Data

Use your own Django project from the [Django Sessions](https://github.com/dci-python-course/Python-basics-django-sessions).

Alternatively, you can use the [solution provided](https://github.com/dci-python-course/Python-basics-django-sessions/tree/solution_task3/solution/course) on the last task of that exercise.

> If you do so, make sure your virtual environment has all the necessary dependencies by moving into the `course` directory and typing:
>
> `(env) $ pip install -r requirements.txt`

## Tasks

### Task 1

Edit the file `common/tests.py` in your repository, and write the code necessary to confirm that all the paths in the common app work as expected (they return a `200` or `302` status code, depending on the view).

You will have to assert that:

- The **home path** returns a `200` status code.
- The **login path** returns a `200` status code.
- The **logout path** returns a `302` status code.
- The **redirect to note details path** returns a `302` status code.

> Make sure that every path has a `name` argument in your `common/urls.py` file.

Once you are done, run all the tests.

**Your output should look like this:**

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....
----------------------------------------------------------------------
Ran 4 tests in 0.020s

OK
Destroying test database for alias 'default'...
```

### Task 2

Now do the same for the `notes` and `todo` apps, editing the files `notes/tests.py` and `todo/tests.py`.

In the notes app, you will have to assert that:

- The **home path** returns a `200` status code.
- The **sections path** returns a `200` status code.
- The (notes) **by section path** returns a `200` status code.
- The **details path** returns a `200` status code.
- The **edit path** returns a `200` status code.
- The **details path** returns a `200` status code.
- The **vote path** returns a `302` status code.
- The **search path** returns a `200` status code.
- The **added ok path** returns a `200` status code.
- The **add path** returns a `200` status code.

In the todo app, you will have to assert that:

- The **details path** returns a `200` status code.

In this case, you can do a single test for all paths that do not require an argument and return a `200` status code (that is: `home`, `sections`, `search`, `add` and `added_ok`).

> Hint: define a tuple with those names and iterate it to assert each response.

For the rest of the cases, use a single test and a valid test argument to process the request. The voting path is the only one that returns a redirection.

Once you have done so, run the tests all at once.

**Your output may look similar to this:**
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......E..
======================================================================
ERROR: test_note_vote_path (notes.tests.PathTestCase)
Check if the note vote path works.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/DCI/Django/exercises/Python-basics-django-tests/solution/course/notes/tests.py", line 43, in test_note_vote_path
    response = self.client.get(reverse("vote", args=[1]))
  File "/home/DCI/Django/env/lib/python3.6/site-packages/django/test/client.py", line 742, in get
    response = super().get(path, data=data, secure=secure, **extra)
  File "/home/DCI/Django/env/lib/python3.6/site-packages/django/test/client.py", line 398, in get
    **extra,
  File "/home/DCI/Django/env/lib/python3.6/site-packages/django/test/client.py", line 473, in generic
    return self.request(**r)
  File "/home/DCI/Django/env/lib/python3.6/site-packages/django/test/client.py", line 719, in request
    self.check_exception(response)
  File "/home/DCI/Django/env/lib/python3.6/site-packages/django/test/client.py", line 580, in check_exception
    raise exc_value
  File "/home/DCI/Django/env/lib/python3.6/site-packages/django/core/handlers/exception.py", line 47, in inner
    response = get_response(request)
  File "/home/DCI/Django/env/lib/python3.6/site-packages/django/core/handlers/base.py", line 181, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/home/DCI/Django/env/lib/python3.6/site-packages/django/views/generic/base.py", line 70, in view
    return self.dispatch(request, *args, **kwargs)
  File "/home/DCI/Django/env/lib/python3.6/site-packages/django/views/generic/base.py", line 98, in dispatch
    return handler(request, *args, **kwargs)
  File "/home/DCI/Django/exercises/Python-basics-django-tests/solution/course/notes/views.py", line 183, in get
    if user["name"] == request.session.get("user_name")].pop(0)
IndexError: pop from empty list

----------------------------------------------------------------------
Ran 9 tests in 0.102s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

This error is produced because on our solution we didn't consider the idea that an unregistered user may request the vote path and we assumed there would always be a session variable named `user_name`.

There is no link on the website for unregistered users, but we should fix the view, so that this returns a message or a redirection, instead of an error.

> This is a good example of why writing tests is a good idea. In this case, the error is not critical, but in other cases it might.

Fix any errors you may find and run again the tests until no error is produced.

**Once you are done, your output should look like this:**

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 0.063s

OK
Destroying test database for alias 'default'...
```

### Task 3

To make better tests on the path resolutions, you should now add additional asserts to the paths that return a `302` status code.

In those cases, write additional code to check which is the redirection target, and make sure the path works and it is the proper one.

You will have to assert that:

- The **logout** path redirects to the **home** path.
- The old non-namespaced note **details** path redirects to the new namespaced **details** path.
- The note **voting** path redirects to the **home** path (we are not logged in).

> You have to assert both that the redirecting path works (returns a `200` status code) and that it is the proper path.
>
> You can add these new assertions on the same methods you already have, after asserting that the first response is a redirection.

**Once you are done, all your tests should pass successfully:**

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..........
----------------------------------------------------------------------
Ran 10 tests in 0.063s

OK
Destroying test database for alias 'default'...
```

### Task 4

There are a couple of paths you did not finish testing. The **login** and **voting** paths should behave differently when the user is logged in.

But before you do that, you should test if the **login** functionality works. That means, that you will have to use the `post` method of the `self.client` object and pass it some `user_name` and `password` (use the admin for this test).

Then, you will have to assert that:

- The response of the POST login request is a redirection.
- The `user_name` variable set in the session is **admin**.
- The session has a `user_votes` key.
- The session has a `user_can_write_votes` key.
- That the key `user_can_write_votes` is set to True.

> **Hint**: you can access the session data after you call the login path and using the `self.client.session` object.

Define this test in a new class method in your `common/test.py`.

Once you have tested the login authentication and the session creation, write another test (in another method) to make sure the user gets redirected to the **home** path when visiting the **login** path again after being authenticated.

Then, do the same for the **vote** path and make sure after voting with an active session the user gets redirected to the details view. In the same test, assert that the session variable `user_votes` has increased the same amount as the amount of calls done to the **vote** path in your test.

**Once you are done, run all tests. The output should look like this:**

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.............
----------------------------------------------------------------------
Ran 13 tests in 0.538s

OK
Destroying test database for alias 'default'...
```

### Task 5

Now write a new test to make sure the log in form field validation works fine. You should assert that both the `user_name` and `password` are required and a form without either of them is not valid.

**Once you are done, run all tests. Your output should look like this:**

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..............
----------------------------------------------------------------------
Ran 14 tests in 0.641s

OK
Destroying test database for alias 'default'...
```

### Task 6

Finally, add the following tags to your tests:

**In common app** add the following tags to:

- **login form**: `form`, `auth`.
- **home path**: `path`.
- **login path**: `path`, `auth`.
- **login authentication**: `session`, `auth`, `redirect`.
- **login path authenticated**: `path`, `session`, `auth`, `redirect`.
- **logout path**: `path`, `session`, `auth`, `redirect`.
- **old details path redirection**: `path`, `redirect`.

**In notes app** add the following tags to:

- **vote path**: `path`, `redirect`.
- **vote path authenticated**: `path`, `redirect`, `session`.
- The **rest of paths**: `path`.

**In notes app** add the following tags to:

- **todo details**: `path`.

Now, write a single command to run the following sets of tests, and compare the output:

- **Test the authentication only**.

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....
----------------------------------------------------------------------
Ran 5 tests in 0.303s

OK
Destroying test database for alias 'default'...
```

- **Run all tests dealing with sessions**.

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....
----------------------------------------------------------------------
Ran 3 tests in 0.303s

OK
Destroying test database for alias 'default'...
```

- **Run all tests in the notes app**.

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....
----------------------------------------------------------------------
Ran 6 tests in 0.303s

OK
Destroying test database for alias 'default'...
```

- **Run the login authentication test only**.

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....
----------------------------------------------------------------------
Ran 1 tests in 0.303s

OK
Destroying test database for alias 'default'...
```
