# V1BuildConfigSpec

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**run_policy** | **str** | RunPolicy describes how the new build created from this build configuration will be scheduled for execution. This is optional, if not specified we default to \&quot;Serial\&quot;. | [optional] 
**triggers** | [**list[V1BuildTriggerPolicy]**](V1BuildTriggerPolicy.md) | triggers determine how new Builds can be launched from a BuildConfig. If no triggers are defined, a new build can only occur as a result of an explicit openshift.client build creation. | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


