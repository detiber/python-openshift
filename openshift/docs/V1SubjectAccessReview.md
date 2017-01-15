# V1SubjectAccessReview

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**groups** | **list[str]** | GroupsSlice is optional. Groups is the list of groups to which the User belongs. | 
**scopes** | **list[str]** | Scopes to use for the evaluation.  Empty means \&quot;use the unscoped (full) permissions of the user/groups\&quot;. Nil for a self-SAR, means \&quot;use the scopes on this request\&quot;. Nil for a regular SAR, means the same as empty. | 
**user** | **str** | User is optional. If both User and Groups are empty, the current authenticated user is used. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


