#!/usr/bin/env python3

#############
# nesttemp.py


import os
import time
import json
import requests
import argparse

account_file = 'account.json'
device_file = 'devices.json'
token_file = 'google_tokens.json'
base_path = os.path.dirname(os.path.realpath(__file__))

def get_account(path='{}/conf'.format(base_path)):
    af = path + '/' + account_file
    with open(af) as account:
        account = json.load(account)
    return account 

def get_devices(path='{}/conf'.format(base_path)):
    df = path + '/' + device_file 
    with open(df) as device:
        devices = json.load(device)
    return devices


def get_tokens(path='{}/conf'.format(base_path)):

    tf = path + '/' + token_file

    #load token files
    with open(tf) as tokenFile:
        google_tokens = json.load(tokenFile)

    # get client_id and client_secret
    account = get_account(path)

    # If current token has expired make post request for new one
    res = requests.post(
        url = 'https://www.googleapis.com/oauth2/v4/token',
        data = {
            'client_id': account['client_id'],
            'client_secret': account['client_secret'],
            'refresh_token': account['refresh_token'],
            'grant_type': 'refresh_token',
            }
        )

    newtokens = res.json()

        #update token file
    with open(tf, 'w') as newGoogleTokens:
        json.dump(newtokens, newGoogleTokens)
        google_tokens = newtokens

    return google_tokens

def build_url(tokens, zone):
    devices = get_devices()
    account = get_account()

    program = account['project_id']
    baseurl = 'https://smartdevicemanagement.googleapis.com/v1/enterprises/{}/devices'.format(program)
    url = '{}/{}:executeCommand'.format(baseurl,devices[zone])
    headers = { 'Authorization' : 'Bearer ' + tokens['access_token'], "Content-Type" : "application/json"}

    return (url, headers)

def set_mode(tokens, mode, zone):
    (url, headers) = build_url(tokens, zone)
    data = {
        'command' : 'sdm.devices.commands.ThermostatMode.SetMode', 
        'params' : {'mode' : mode}
    }

    res = requests.post(url, headers=headers, data=json.dumps(data))
    print(res.content)

def set_heat(tokens, temp, zone):
    (url, headers) = build_url(tokens, zone)
    data = {
        'command' : 'sdm.devices.commands.ThermostatTemperatureSetpoint.SetHeat', 
        'params' : {'heatCelsius' : temp}
    }

    res = requests.post(url, headers=headers, data=json.dumps(data))
    print(res.content)

def set_cool(tokens, temp, zone):
    (url, headers) = build_url(tokens, zone)
    data = {
        'command' : 'sdm.devices.commands.ThermostatTemperatureSetpoint.SetCool', 
        'params' : {'coolCelsius' : temp}
    }

    res = requests.post(url, headers=headers, data=json.dumps(data))
    print(res.content)

def set_temp_point(tokens, low, high, zone):
    (url, headers) = build_url(tokens, zone)
    data = {
        'command' : 'sdm.devices.commands.ThermostatTemperatureSetpoint.SetRange', 
        'params' : {'heatCelsius' : low, 'coolCelsius' : high}
    }

    res = requests.post(url, headers=headers, data=json.dumps(data))
    print(res.content)

#####

parser = argparse.ArgumentParser(description='Nest Controller.')
parser.add_argument('-m', '--min', type=int, help='heat to min (range)')
parser.add_argument('-n', '--max', type=int, help='cool to max (range)')
parser.add_argument('-t', '--heat', type=int, help='heat to temp')
parser.add_argument('-c', '--cool', type=int, help="cool to temp") 
parser.add_argument('-d', '--mode', type=str, help="set mode") 
parser.add_argument('-z', '--zone', type=str, help="zone") 
args = parser.parse_args()

tokens = get_tokens()

if args.zone:
    zone = args.zone
else:
    zone = 'upstairs'

if args.min:
    set_mode(tokens,'HEATCOOL', zone)
    set_temp_point(tokens, args.min, args.min+1.5, zone)
elif args.max:
    set_mode(tokens,'HEATCOOL', zone)
    set_temp_point(tokens, args.max-2, args.max, zone)
elif args.heat:
    set_mode(tokens,'HEAT', zone)
    set_heat(tokens,args.heat, zone)
elif args.cool:
    set_mode(tokens,'COOL', zone)
    set_cool(tokens,args.cool, zone)
else:
    set_mode(tokens,'HEATCOOL', zone)
    set_temp_point(tokens, 20,22)

