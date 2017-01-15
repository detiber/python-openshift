# V1ClusterNetwork

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hostsubnetlength** | **int** | HostSubnetLength is the number of bits of network to allocate to each node. eg, 8 would mean that each node would have a /24 slice of the overlay network for its pods | 
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. | [optional] 
**network** | **str** | Network is a CIDR string specifying the global overlay network&#39;s L3 space | 
**plugin_name** | **str** | PluginName is the name of the network plugin being used | [optional] 
**service_network** | **str** | ServiceNetwork is the CIDR range that Service IP addresses are allocated from | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


