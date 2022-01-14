
# License Node Information REST API Design

GET /V2/System/nodeinfo
-----------------------

Call this API to get the overall system license node information.

User must have System Admin privilege to issue this API call.

Detail Information
------------------

> Title: License Node Information API

> Version: 03/09/2021

> API Server URL: http(s)://IP Address of NetBrain Web API
Server/ServicesAPI/API/V2/System/nodeinfo

> Authentication:

| **Type**              | **In**  | **Name**             |
|-----------------------|---------|----------------------|
| Bearer Authentication | Headers | Authentication token |

Request body (\*required)
-------------------------

> No parameters required.

Query Parameters (\*required)
-----------------------------

> No parameters required.

Path Parameters (\*required)
-----------------------------
| **Name**     | **Type** | **Description**                                        |
|--------------|----------|--------------------------------------------------------|
| tenantId     | String   | To get the license information of the specified tenant |
| domainId     | String   | To get the license information of the specified domain |

Headers
-------

> Data Format Headers

| **Name**     | **Type** | **Description**            |
|--------------|----------|----------------------------|
| Content-Type | String   | Support “application/json” |
| Accept       | String   | Support “application/json” |

> Authorization Headers

| **Name** | **Type** | **Description**                           |
|----------|----------|-------------------------------------------|
| Token    | String   | Authentication token, get from login API. |

Response
--------

| **Name**       | **Type**         | **Description**                        |
|----------------|------------------|----------------------------------------|
| module         | Array of objects | Module list                            |
| module.name    | String           | Module name                            |
| module.nodes   | Integer          | License node the module needs          |
| module.enabled | Bool             | Whether or not the module is enabled   |
| tech           | Array of objects | Network technology list                |
| tech.name      | String           | Network technology name                |
| tech.total     | Integer          | Network technology total license nodes |
| tech.used      | Integer          | Network technology used license nodes  |

***Note: Error Code clarification***

| **Code** | **Message** |
|------------------------------------|----------|
| 790200 | Success |
| 795012 | License is expired. |
| 793001 | System framework level error. |


***Example***


```python
{
    "totalMaximumNodes": 11570000,
    "totalFreeNodes": 0,
    "totalUsedNodes": 11570000,
    "tenants": [
        {
            "tenantId": "088e3cc5-f508-11c3-8f7d-665a3f8de509",
            "tenantName": "Initial Tenant",
            "description": "This is the initial tenant",
            "tenantMaximumNodes": 11570000,
            "tenantFreeNodes": 11560000,
            "tenantUsedNodes": 10000,
            "domains": [
                {
                    "domainId": "b986a07f-f128-453e-ba08-5497ba8ab8fa",
                    "domainName": "Domain1",
                    "description": "",
                    "domainMaximumNodes": 10000,
                    "domainFreeNodes": 9919,
                    "domainUsedNodes": 81
                }
            ]
        }
    ],
    "statusCode": 790200,
    "statusDescription": "Success."
}
```

# Full Example


```python
# import python modules 
import requests
import time
import urllib3
import pprint
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json

token = "87ccc8aa-6550-41cd-a54b-ae11b521a837" 
 
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}  
headers['token'] = token
full_url = "http://192.168.28.139/ServicesAPI/API/V1/System/nodeinfo"

try:
    # Do the HTTP request
    response = requests.get(full_url, headers=headers, verify=False)
    # Check for HTTP codes other than 200
    if response.status_code == 200:
        # Decode the JSON response into a dictionary and use the data
        js = response.json()
        print (js)
    else:
        print ("Get Node Information failed! - " + str(response.text))
except Exception as e:
    print (str(e))
```

    {'totalMaximumNodes': 11570000, 'totalFreeNodes': 0, 'totalUsedNodes': 11570000, 'tenants': [{'tenantId': '088e3cc5-f508-11c3-8f7d-665a3f8de509', 'tenantName': 'Initial Tenant', 'description': 'This is the initial tenant', 'tenantMaximumNodes': 11570000, 'tenantFreeNodes': 11560000, 'tenantUsedNodes': 10000, 'domains': [{'domainId': 'b986a07f-f128-453e-ba08-5497ba8ab8fa', 'domainName': 'Domain1', 'description': '', 'domainMaximumNodes': 10000, 'domainFreeNodes': 9919, 'domainUsedNodes': 81}]}], 'statusCode': 790200, 'statusDescription': 'Success.'}
    

# cURL Code from Postman


```python
curl --location --request GET 'http://192.168.28.139/ServicesAPI/API/V1/System/nodeinfo' \
--header 'token: 87ccc8aa-6550-41cd-a54b-ae11b521a837'
```
