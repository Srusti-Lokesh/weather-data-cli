# Weather Data CLI

A Python command-line application that fetches current weather for a user-provided city from the OpenWeatherMap API. This repository also includes a lightweight Flask web interface so the same weather service can be deployed and demonstrated on Render.

## Features

- Current temperature, feels-like temperature, conditions, humidity, wind speed, and pressure
- City input through CLI arguments or an interactive prompt
- JSON response parsing and readable terminal output
- Friendly handling for invalid cities, missing/invalid API keys, timeouts, network failures, provider errors, and rate limits
- API key supplied through an environment variable (never commit secrets)
- Responsive web page and `/health` endpoint for Render
- Unit tests for response parsing and common errors

## Technology

Python 3, `requests`, Flask, Gunicorn, OpenWeatherMap Current Weather API, pytest, Render.

## Requirements

- Python 3.10 or newer
- An OpenWeatherMap API key (the provider may take time to activate a newly created key)
- Internet access

## Run on Windows PowerShell

Open PowerShell in the extracted project folder.

```powershell
py --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use this for the current terminal only, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Set the API key for the current PowerShell session (replace the example with your actual key):

```powershell
$env:OPENWEATHER_API_KEY = "YOUR_REAL_API_KEY"
```

CLI examples:

```powershell
python .\weather_cli.py Bengaluru
python .\weather_cli.py "New York"
python .\weather_cli.py
```

Run the web interface locally:

```powershell
python .\app.py
```

Open `http://127.0.0.1:5000` in your browser. Stop the server with `Ctrl+C`.

Run tests (optional test dependency):

```powershell
pip install pytest
python -m pytest -q
```

## Get an API key

1. Create an account on the official OpenWeatherMap website: https://openweathermap.org/.
2. Find the API keys section in your account and create/copy a key for the Current Weather API.
3. Store it only in your environment or Render environment settings. Do not paste it into source code, screenshots, README files, or Git commits.
4. If the key returns 401 immediately after creation, allow time for provider activation and re-check the key.

## GitHub submission

Create a **public** repository named `weather-data-cli` (unless your internship portal specifies another naming convention). Suggested repository description:

> A Python weather CLI using the OpenWeatherMap API, with formatted current-weather output, robust error handling, and a Flask web demo deployable on Render.

From PowerShell, inside the project directory:

```powershell
git init
git add .
git status
git commit -m "Build weather data CLI with API integration"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/weather-data-cli.git
git push -u origin main
```

Replace `YOUR-GITHUB-USERNAME` with your real GitHub username. If Git says `remote origin already exists`, run `git remote -v`; if the URL is wrong, use `git remote set-url origin https://github.com/YOUR-GITHUB-USERNAME/weather-data-cli.git`. Do not commit `.env` or your API key.

## Deploy to Render

This project is a CLI, but hosted CLI programs have no interactive terminal for visitors. Therefore, a small Flask interface is included for a practical public demo. The CLI remains runnable locally.

1. Push the project to GitHub using the commands above.
2. Sign in to Render and choose **New + → Web Service**.
3. Connect your GitHub account and select `weather-data-cli`.
4. Configure:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. In Render service **Environment**, add `OPENWEATHER_API_KEY` with your real API key. Do not put the key in `render.yaml` or GitHub.
6. Create/deploy the service and wait for the deploy status to show **Live**.
7. Open the Render-provided `https://...onrender.com` URL, search for a city, and check that weather data appears.
8. Check `https://YOUR-RENDER-SERVICE.onrender.com/health`; it should return `{"status":"ok"}`.
9. If deployment fails, open Render → service → **Logs**. Verify the build/start commands, Python dependencies, and environment variable. Redeploy after fixing settings.

The included `render.yaml` documents the service configuration; you can either configure the dashboard manually or use Render Blueprint deployment. Render plan availability and free-tier limits can change, so confirm current options in your Render dashboard.

## Submission checklist

- [ ] Run the CLI successfully with a valid API key.
- [ ] Test a deliberately invalid city and verify a useful error appears.
- [ ] Run `python -m pytest -q` and save the passing result if tests are available.
- [ ] Push all source files to a **public** GitHub repository.
- [ ] Deploy the Flask demo on Render and verify the public URL and `/health`.
- [ ] Add the final GitHub repository URL and Render URL to your submission notes/portal.
- [ ] Include deployment configuration, rollback evidence, and this README as required by the internship instructions.
- [ ] For rollback evidence, capture the Render Events/deploy history showing the successful deployment and, if you perform a rollback, the selected prior successful deploy. Do not claim a rollback was done unless it actually was.
- [ ] Publish the LinkedIn project post after deployment and include the working repository/demo links.
- [ ] Never publish API keys, account tokens, or private information.

## Troubleshooting

- **`python` is not recognized:** install Python 3.10+ and enable “Add Python to PATH”, then reopen PowerShell. `py` may work even when `python` does not.
- **Activation is disabled:** use the process-scoped execution policy command above; it affects only the current PowerShell process.
- **401 Unauthorized:** verify the API key, and wait if it is newly created.
- **404 city not found:** check spelling; try a city name with country code if needed, for example `Paris,FR`.
- **429 Too Many Requests:** wait and retry later.
- **Render page reports missing key:** confirm `OPENWEATHER_API_KEY` exists in Render Environment and redeploy/restart.
- **Render deploy fails:** inspect logs and confirm `gunicorn app:app` is the start command.

## API behavior and limitations

The app requests metric units, so temperatures are Celsius and wind speed is metres per second. It displays current conditions, not forecasts. Availability and rate limits are controlled by the API provider. This project does not include persistent storage.

## Interview questions

**How do APIs authenticate requests?** This app sends the API key as the `appid` query parameter over HTTPS. API providers may also support bearer tokens or other schemes.

**What happens when an API returns 404?** The application interprets it as a city that could not be found and displays a user-friendly message.

**How would you handle API rate limits?** Detect HTTP 429, communicate the issue, respect any `Retry-After` header, add bounded exponential backoff where appropriate, and cache responses when allowed by provider terms.
