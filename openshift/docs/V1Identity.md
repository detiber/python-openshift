# V1Identity

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**extra** | **dict(str, str)** | Extra holds extra information about this identity | [optional] 
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. | [optional] 
**provider_name** | **str** | ProviderName is the source of identity information | 
**provider_user_name** | **str** | ProviderUserName uniquely represents this identity in the scope of the provider | 
**user** | [**V1ObjectReference**](V1ObjectReference.md) | User is a reference to the user this identity is associated with Both Name and UID must be set | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


