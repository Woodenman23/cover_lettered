# Cover Letter AI

This is the application to enable users to automate the production of targeted cover letters when applying to jobs.

It is a flask application that:

- Takes inputs from user about their skills and experience, as well as a role description
- Generates a cover letter that is tailored to the confluence of the applicant's skills and the employer's requirements
- Tracks applicant's previous letters

This project is open source, use it as a template to build your own application
if you wish. Or check out this [free tutorial](https://youtu.be/mqhxxeeTbu0?si=OicLhr4NVffZhQWZ)
with techwithtim to start at the same place I did.

## Installation

Alternatively the app can be run locally by following these steps:

1. clone the repo
2. add .api_keys.yaml to the project root
   ...
3. build the docker image: `docker build . -t flask-ai .`
4. run the image: `docker run flask-ai`
