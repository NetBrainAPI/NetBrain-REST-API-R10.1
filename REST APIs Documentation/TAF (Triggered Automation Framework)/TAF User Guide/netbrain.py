# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 15:26:49 2022

@author: songh
"""

# import json
from requests import Session, packages
from urllib.parse import urljoin
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class NBRequestSessionBase(Session):
    def __init__(self, prefix_url):
        self.prefix_url = prefix_url.rstrip("/") + "/"
        super(NBRequestSessionBase, self).__init__()
        self.verify = False
        self.user = {}

    def request(self, method, url, *args, **kwargs):
        if url.startswith("http://") or url.startswith("https://"):
            url = url.strip()
        else:
            url = urljoin(self.prefix_url, url.lstrip("/"))

        if self.user.get('token', None) is not None:
            self.headers.update({"Token": self.user['token']})        
            
        self.headers.update({"Content-Type":"application/json","Accept":"application/json"})

        return super(NBRequestSessionBase, self).request(method, url, * args, **kwargs)

    def get_tenant_guid_by_name(self, tenant_name):
        url = '/API/V1/CMDB/Tenants'
        data = self.get(url).json()
        # print(data['tenants'])
        if len(data['tenants']) > 0:
            for tenant in data['tenants']:
                if tenant['tenantName'] == tenant_name:
                    return tenant['tenantId']
        return None

    def get_domain_guid_by_name(self, tenant_guid, domain_name):
        url = '/API/V1/CMDB/Domains?tenantId=' + tenant_guid
        data = self.get(url).json()
        # print(data['domains'])
        if len(data['domains']) > 0:
            for domain in data['domains']:
                if domain['domainName'] == domain_name:
                    return domain['domainId']
        return None

    def set_tenant_domain_guid(self, tenant_guid, domain_guid):
        # if tenant_guid is not None and domain_guid is not None:
        if tenant_guid is None:
            raise ValueError("tenant_guid must not empty!")
        self.headers.update({"TenantGuid": tenant_guid})

        if domain_guid is not None:
            self.headers.update({"DomainGuid": domain_guid})


class LegacyThirdPartyAPIRequestSession(NBRequestSessionBase):

    def set_token(self, token):
        self.user["token"] = token

    def login(self, username, password):
        response = self.post('/API/V1/Session',
                      auth=(username, password)).json()
        if response["statusCode"] == 790200:
            self.user["token"] = response["token"]
        else:
            raise ValueError(response["statusDescription"])
    
    def logout(self):
        self.delete("/API/V1/Session")
    
    def set_tenant_domain(self,tenant_name,domain_name):
        tenant_guid = self.get_tenant_guid_by_name(tenant_name)
        domain_guid = self.get_domain_guid_by_name(tenant_guid,domain_name)
        self.set_tenant_domain_guid(tenant_guid,domain_guid)
        
    def get_product_version(self):
        return self.get("/API/v1/System/ProductVersion").json()
        
    def create_event_metadata(self, event_metadata):
        response = self.post("/API/V1/TAF/AutoMapping",
                             data = json.dumps(event_metadata)).json()
        if response:
            return "Succeeded"
        else:
            raise ValueError(response["statusDescription"])
    
    def set_taf_scope(self, scope=None, tenant_name=None, domain_name=None):
        option = {}
        if any([scope, tenant_name, domain_name]):
            if scope is None:
                if all([tenant_name, domain_name]):
                    tenant_guid = self.get_tenant_guid_by_name(tenant_name)
                    domain_guid = self.get_domain_guid_by_name(tenant_guid,
                                                               domain_name)
                    option["tenandId"] = tenant_guid
                    option["domainId"] = domain_guid
                else:
                    raise ValueError("Either tenant_name or domain_name \
                                     is not provided.")
            else:
                option["scope"] = scope
        else:
            raise ValueError("Please provide scope or tenant_name & domain_name.")
        return option
    
    def publish_event(self, event_data, source, category,
                      scope=None, tenant_name=None, domain_name=None):
        """document test"""
        body = {
            "specificData":event_data,
            "option":{
                "source":source,
                "category":category
                }
            }
        
        option = self.set_taf_scope(scope=scope,tenant_name=tenant_name,
                                    domain_name=domain_name)
        body["option"] = {**body["option"], **option}
   
        response = self.post("/API/V1/TAF/Auto",
                             data=json.dumps(body)).json()
        if response["statusCode"] == 790200:
            return response
        else:
            raise ValueError(response["statusDescription"])
    
    def get_trigger_result(self, taskId):
        body = {
            "option":{
                "scope":"Demo",
                "taskId":taskId
                }
            }
        response = self.post("/API/V1/TAF/Result",
                              data=json.dumps(body)).json()
        if response["statusCode"] == 790200:
            return response
        else:
            raise ValueError(response["statusDescription"])
            
    def get_diagnosis_definition(self, scope=None, tenant_name=None, 
                                 domain_name=None, type=1):
        body = {"type":type}
        
        option = self.set_taf_scope(scope=scope,tenant_name=tenant_name,
                                    domain_name=domain_name)
        body["option"] = option
        
        response = self.post("/API/V1/TAF/ManuallyDiagnosis",
                             data=json.dumps(body)).json()
        if response["statusCode"] == 790200:
            return response
        else:
            raise ValueError(response["statusDescription"])
            
    def manual_trigger(self, event_data, source, category,
                       manuallyParams, diagnosisId, scope=None, 
                       tenant_name=None, domain_name=None):
        body = {
            "specificData":event_data,
            "option":{
                "source":source,
                "category":category,
                "diagnosisId":diagnosisId,
                "manuallyParams":manuallyParams
                }
            }
        
        option = self.set_taf_scope(scope=scope,tenant_name=tenant_name,
                                    domain_name=domain_name)
        body["option"] = {**body["option"], **option}
   
        response = self.post("/API/V1/TAF/Manually",
                             data=json.dumps(body)).json()
        if response["statusCode"] == 790200:
            return response
        else:
            raise ValueError(response["statusDescription"])
            
    def update_inc_message(self, event_data, source, category,
                           nbIncidentId, scope=None, tenant_name=None,
                           domain_name=None):
        body = {
            "specificData":event_data,
            "option":{
                "source":source,
                "category":category,
                "nbIncidentId":nbIncidentId
                }
            }
        
        option = self.set_taf_scope(scope=scope,tenant_name=tenant_name,
                                    domain_name=domain_name)
        body["option"] = {**body["option"], **option}
   
        response = self.post("/API/V1/TAF/Updated",
                             data=json.dumps(body)).json()
        if response["statusCode"] == 790200:
            return response
        else:
            raise ValueError(response["statusDescription"])
            
    def check_user_permission(self, tenantName, domainName, privileges=["systemManagement"]):
        """
        Validate user permission to ensure the selected API user has
        sufficient privileges to perform the triggered automation against
        NetBrain TAF. (systemManagement is required for TAF)
        :privileges: privilege names, list
        systemManagement
        domainAdmin
        accessToLiveNetwork
        """
        
        tenantId = self.get_tenant_guid_by_name(tenantName)
        domainId = self.get_domain_guid_by_name(tenantId, domainName)
        
        body = {
            "tenantId":tenantId,
            "domainId":domainId,
            "permissions":privileges
            }
        response = self.post("/API/V1/CMDB/Users/checkPermission",
                             data=json.dumps(body)).json()
        
        if response["statusCode"] == 0:
            return response["privileges"]
        else:
            raise ValueError(response["statusDescription"])