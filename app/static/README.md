# JobMatch Prototype

This is a frontend-only prototype for the job matching platform.

## Included pages

- Landing page
- Login page
- Registration page
- Candidate profile form
- Candidate homepage
- Job search by job description only
- Top 10 recommended jobs using mock data
- Employer job posting form
- Employer homepage
- Candidate search and filters
- Top 10 recommended candidates using mock data

## How to run

Open `index.html` in a web browser.

No backend, database, authentication, or real AI recommendation system is included yet.

## Backend integration later

The mock data in `app.js` can later be replaced with API calls such as:

```js
fetch('/api/jobs')
fetch('/api/candidates')
fetch('/api/recommended-jobs')
fetch('/api/recommended-candidates')
```


## Latest update

Dynamic header/navigation has been added. Public pages show public actions such as Login/Register, while Candidate and Employer pages show role-specific dashboard actions and Logout instead.
