# V1OAuthClientAuthorization

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**openshift.client_name** | **str** | ClientName references the openshift.client that created this authorization | [optional] 
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. | [optional] 
**scopes** | **list[str]** | Scopes is an array of the granted scopes. | [optional] 
**user_name** | **str** | UserName is the user name that authorized this openshift.client | [optional] 
**user_uid** | **str** | UserUID is the unique UID associated with this authorization. UserUID and UserName must both match for this authorization to be valid. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


