# Project Report: Weather Data CLI

## Abstract
Weather Data CLI is a Python application that retrieves current weather conditions for a city through the OpenWeatherMap Current Weather API. It demonstrates HTTP requests, API authentication, JSON parsing, command-line argument handling, output formatting, and exception handling. A small Flask interface is included to make the project accessible as a Render-hosted web demo while preserving the original CLI workflow.

## Problem statement
Users need a simple way to retrieve current weather information for a chosen city. The application should accept user input, request data from a weather API, show useful values, and fail gracefully when a city or request is invalid.

## Objectives
- Build a command-line weather lookup tool.
- Integrate a third-party API securely.
- Parse JSON into a small, predictable data structure.
- Display temperature, feels-like temperature, condition, humidity, wind speed, and pressure.
- Handle expected API/network errors clearly.
- Provide a deployable web demonstration and repeatable setup instructions.

## Tools and technologies
Python 3; Requests for HTTP; OpenWeatherMap Current Weather API; Flask for the web view; Gunicorn for production serving; pytest for unit tests; Git/GitHub for version control; Render for hosting.

## Architecture and workflow
1. The user supplies a city through CLI arguments or a web form.
2. The application reads `OPENWEATHER_API_KEY` from the environment.
3. Requests sends an HTTPS request with city, API key, and metric units.
4. The application checks the response status and parses JSON.
5. Selected fields are normalized into a dictionary.
6. The CLI prints readable text or the Flask page renders a responsive weather card.
7. Expected failures become clear error messages instead of raw tracebacks.

## Implementation details
The `fetch_weather` function isolates network access and response parsing. A timeout limits how long the program waits for the provider. HTTP 404, 401, 429, and server errors receive specific messages. The API key is not hard-coded; local development uses a PowerShell environment variable, while Render uses its Environment settings. The Flask `/health` endpoint provides a simple service-health response.

## Validation and testing
Automated unit tests cover successful JSON parsing, missing credentials, city-not-found responses, and formatted output. Before submission, run `python -m pytest -q`, test one valid city using an active key, test an invalid city, and verify the deployed `/health` endpoint. Actual live API and hosting checks must be performed by the project owner; this report does not claim a deployment or test run that has not been performed.

## Deployment
The repository contains `render.yaml` and uses `pip install -r requirements.txt` as the build command and `gunicorn app:app` as the start command. The owner must connect the public GitHub repository to Render, set `OPENWEATHER_API_KEY` as a secret environment variable, deploy, and verify the generated URL.

## Security and error handling
Credentials are read from the environment and `.env` files are ignored by Git. Network calls use a timeout. The app handles common authentication, city lookup, rate-limit, network, and provider failures. API keys should never be included in source files, commits, public screenshots, or LinkedIn posts.

## Limitations and future improvements
The project currently reports current conditions only, depends on the provider's service and rate limits, and does not cache responses or persist history. Possible extensions include forecast support, bounded retries for transient errors, caching, location disambiguation, richer tests, and accessibility improvements.

## Conclusion
This project demonstrates a practical end-to-end Python API workflow, from input and HTTP requests through JSON processing, error handling, output formatting, tests, source control, and cloud deployment configuration. Successful live operation depends on adding a valid API key and completing the user's GitHub and Render setup.
