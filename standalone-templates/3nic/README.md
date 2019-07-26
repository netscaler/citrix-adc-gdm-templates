# Deploy three NIC Citrix ADC using Google Deployment Manager
You can deploy a Citrix ADC VPX instance on Google Cloud Platform (GCP).  A VPX instance in GCP enables you to leverage cloud computing capabilities of GCP and use Citrix load balancing and traffic management features for your business needs. You can deploy VPX instances in GCP as standalone instances.

## Introduction
This template deploys a Citrix ADC instance with three NICs. Each NIC handles management, client, and server traffic respectively.

### Prerequisites
1. A subscription to Google Cloud Platform.
2. Install [Google SDK](https://cloud.google.com/sdk/install) to access the "gcloud" utility.
3. Citrix ADC BYOL license based on your requirements.
4. Three network and three subnets within the networks under VPC Network.
5. A Citrix ADC image on Google Cloud Platform.
 	1. For marketplace image, please refer to the table below.
	2. Details to create a custom image image can be found [here](https://docs.citrix.com/en-us/netscaler/12-1/deploying-vpx/deploy-vpx-google-cloud.html).

### Citrix ADC Marketplace Images

| Release | Image Name | Project Name | URL |
| --- | --- | --- | --- |
| `13.0` | nsvpx-gcp-13-0-36-102-public | citrix-master-project | https://www.googleapis.com/compute/v1/projects/citrix-master-project/global/images/nsvpx-gcp-13-0-36-102-public |

### Deploy a Citrix ADC VPX instance
You would find three files under this directory. A YAML configuration file, a Python template, and a schema. Note the following points before you start.

1.	Ensure you meet the prerequisites given in the "Prerequisites" section.
2.	Edit the configuration.yml file.
	1.  Refer to the template.py.schema file to understand the variables(keys) present in the YAML file.
	2.	Populate/edit the variables (keys) present in the configuration.yml file to suite your needs.
3.	Deploy the Citrix ADC VPX instance
	1.	Use the following command to deploy the instance.<br>
	    gcloud deployment-manager deployments create <deployment_name> --config configuration.yml
	2.	For more information refer https://cloud.google.com/deployment-manager/docs/
4.	View the outputs (The Citrix ADC parameters). Use the following commands to view the instance that include the external/internal IPs.
	1.	Run the command,<br>
	    gcloud deployment-manager deployments describe <deployment_name> | grep manifest:
	2.	Fetch the manifest ID from the output of the above command.<br>
	    Example: manifest: manifest-1542970019879
	3.	Run the following command.<br>
	    gcloud deployment-manager manifests describe <manifest_id> --deployment <deployment_name> --format="value(layout)"
	4.	In the output, under the outputs section the details regarding the Citrix ADC, specifically the internal/external IPs can be found.

## Troubleshooting
1.	Refer to the template.py.schema file to make sure the variables types are adhered to while editing configuration.yml.
2.	Make sure all the values within configuration.yml are placed within double quotes.
3.	There might be possible indentation errors while editing the configuration files or the python template if it was opened with an intention to edit.
