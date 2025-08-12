# Log Manager microservice

Designed to collect different types of logs from different sources, store them in a database and perform conveniate log queries with different conditions.
<img width="1104" height="491" alt="image" src="https://github.com/user-attachments/assets/05a9bc60-f97a-404a-9882-8934ec5ffd32" />
<img width="1202" height="514" alt="image" src="https://github.com/user-attachments/assets/235a2a67-12c2-4120-afab-8a937ce863b9" />
- Tech stack is: FastAPI, Postgresql, SQLAlchemy and Jinja2
- All requirements are in pyproject.toml (use uv packet manager)
- All environment variables are described in config.py
- log_setups.py contains everything about logs: where to find them, how to connect and how to parse

