# Nest Control

This is a simple script to control modes and temperature set points on a Nest Thermostate using the Google Smart Device Management API.

## Usage

```
usage: nesttemp.py [-h] [-m MIN] [-n MAX] [-t HEAT] [-c COOL] [-d MODE]

Nest Controller.

optional arguments:
  -h, --help            show this help message and exit
  -m MIN, --min MIN     heat to min (range)
  -n MAX, --max MAX     cool to max (range)
  -t HEAT, --heat HEAT  heat to temp
  -c COOL, --cool COOL  cool to temp
  -d MODE, --mode MODE  set mode
```

## Setup 

1. Create a project in Google Cloud Platform: https://developers.google.com/nest/device-access/get-started
    * Create a project
    * Enable the Smart Device Management API
    * Get an OAuth 2.0 Client ID
    * Enable redirects from https://www.google.com/
    * Enable a test user (e.g., your google account <user@google.com>)
    
2. Create a device access project: https://console.nest.google.com/device-access
    * Note the Project ID (needed in subsequent steps)
    
3. Authorize an account to get a code ([details](https://developers.google.com/nest/device-access/authorize))
    * include: client_id (GCP OAuth Client ID from above)
    * `https://nestservices.google.com/partnerconnections/[PROJECT-ID]/auth?redirect_uri=https://www.google.com&access_type=offline&prompt=consent&client_id=[OAUTH-CLIENT-ID]&response_type=code&scope=https://www.googleapis.com/auth/sdm.service`
    
4. Copy the access code (`code`) parameter from the redirect URL and save the tokens:

`curl -L -X POST 'https://www.googleapis.com/oauth2/v4/token?client_id=[OAUTH-CLIENT-ID]&client_secret=[CLIENT-SECRET]&code=[AUTH-CODE]&grant_type=authorization_code&redirect_uri=https://www.google.com' > google_tokens.json`

5. Authorize the application with a simple request that asks for devices.
   Replace the Bearer with the access_token from Step 4 in the request below:
`curl -X GET 'https://smartdevicemanagement.googleapis.com/v1/enterprises/[PROJECT-ID]/devices' -H 'Content-Type: application/json' -H 'Authorization: Bearer [ACCESS-TOKEN]'`
 
6. Refresh Token
    * client_id from GCP/Device Access
    * client_secret from GCP 
    * refresh_token from Step 4

  `curl -L -X POST 'https://www.googleapis.com/oauth2/v4/token?client_id=[OAUTH-CLIENT-ID]&client_secret=[CLIENT-SECRET]&refresh_token=[REFRESH-TOKEN]&grant_type=refresh_token'`
  
  7. Control Devices ([API](https://developers.google.com/nest/device-access))
  You can use the device IDs from Step 4 as a starting point.
  
  `curl -X POST 'https://smartdevicemanagement.googleapis.com/v1/enterprises/[PROJECT-ID]/devices/[DEVICE-ID]:executeCommand' -H 'Content-Type: application/json' -H 'Authorization: Bearer [ACCESS-TOKEN]' --data '{ "command" : "sdm.devices.commands.ThermostatTemperatureSetpoint.SetRange", "params" : { "heatCelsius" : 20.0, "coolCelsius" : 22.0 } }'`

`curl -X POST 'https://smartdevicemanagement.googleapis.com/v1/enterprises/[PROJECT-ID]/devices/[DEVICE-ID]:executeCommand' -H 'Content-Type: application/json' -H 'Authorization: Bearer [ACCESS-TOKEN]' --data '{ "command" : "sdm.devices.commands.ThermostatMode.SetMode", "params" : { "mode" : "HEAT" } }'`

