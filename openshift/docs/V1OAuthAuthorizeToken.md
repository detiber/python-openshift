# V1OAuthAuthorizeToken

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**openshift.client_name** | **str** | ClientName references the openshift.client that created this token. | [optional] 
**code_challenge** | **str** | CodeChallenge is the optional code_challenge associated with this authorization code, as described in rfc7636 | [optional] 
**code_challenge_method** | **str** | CodeChallengeMethod is the optional code_challenge_method associated with this authorization code, as described in rfc7636 | [optional] 
**expires_in** | **int** | ExpiresIn is the seconds from CreationTime before this token expires. | [optional] 
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. | [optional] 
**redirect_uri** | **str** | RedirectURI is the redirection associated with the token. | [optional] 
**scopes** | **list[str]** | Scopes is an array of the requested scopes. | [optional] 
**state** | **str** | State data from request | [optional] 
**user_name** | **str** | UserName is the user name associated with this token | [optional] 
**user_uid** | **str** | UserUID is the unique UID associated with this token. UserUID and UserName must both match for this token to be valid. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


