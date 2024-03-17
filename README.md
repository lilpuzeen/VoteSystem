# Voting System

This is FastAPI project, which is a simple voting system. It allows to create polls, vote for options and see results.


## Installation
Clone the repository using:
```bash
git clone https://github.com/lilpuzeen/VoteSystem.git
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies from pyproject.toml file:

```bash
python -m pip install .
```

Soon, project will be deployed to **Heroku/Render**, so you can use it without installation.

## Quick overview
This project provides a simple RESTful API for creating and participating in various surveys. 
You can create your own survey, add any questions to it and specify answer options for them.

## Usage
To start the project, run the following command:
```bash
uvicorn src.main:app --reload
```
Then go to http://localhost:8000/docs to see the documentation and try the API.



## Project structure
The project is structured as follows:
```
├── VoteSystem
│   ├── .github (contains github actions such as linters, in future will contain CI/CD pipeline)
│   ├── alembic (contains database migrations)
│   ├── src
│   │   ├── actions (contains actions for working with polls and questions)
│   │   ├── auth (contains authentication and authorization, made with JWT and fastapi_users)
│   │   ├── polls (contains polls and questions models, routers and services)
│   │   ├── config.py (contains project settings such as secret key, database url, etc.)
│   │   ├── database.py (contains database connection)
│   │   ├── main.py (contains FastAPI app and routers)
│   ├── docs (contains project documentation, mkdocs will be used in future to generate documentation)
│   ├── tests (still in development)
│   ├── Dockerfile/docker-compose.yml (still in development)
│   ├── etc.
```

## Remaining tasks
- Finalize some CRUD endpoints
- Add tests with pytest (unit, integration, e2e)
- Finalize Dockerfile and docker-compose.yml
- Add aioredis for caching
- slowapi for rate limiting
- Add mkdocs for documentation generation and deploy it to github pages
- Optional: add CORS middleware for frontend and deploy project to Heroku/Render

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

This project will be updated and improved. In the near future it will be possible to work with classes, exceptions, context managers, async and other features.

## License

[MIT](https://choosealicense.com/licenses/mit/)