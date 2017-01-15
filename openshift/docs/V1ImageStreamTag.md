# V1ImageStreamTag

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**conditions** | [**list[V1TagEventCondition]**](V1TagEventCondition.md) | Conditions is an array of conditions that apply to the image stream tag. | [optional] 
**generation** | **int** | Generation is the current generation of the tagged image - if tag is provided and this value is not equal to the tag generation, a user has requested an import that has not completed, or Conditions will be filled out indicating any error. | 
**image** | [**V1Image**](V1Image.md) | Image associated with the ImageStream and tag. | 
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. | [optional] 
**tag** | [**V1TagReference**](V1TagReference.md) | Tag is the spec tag associated with this image stream tag, and it may be null if only pushes have occurred to this image stream. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


