# V1Template

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**labels** | **dict(str, str)** | labels is a optional set of labels that are applied to every object during the Template to Config transformation. | [optional] 
**message** | **str** | message is an optional instructional message that will be displayed when this template is instantiated. This field should inform the user how to utilize the newly created resources. Parameter substitution will be performed on the message before being displayed so that generated credentials and other parameters can be included in the output. | [optional] 
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. | [optional] 
**objects** | [**list[RuntimeRawExtension]**](RuntimeRawExtension.md) | objects is an array of resources to include in this template. | 
**parameters** | [**list[V1Parameter]**](V1Parameter.md) | parameters is an optional array of Parameters used during the Template to Config transformation. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


