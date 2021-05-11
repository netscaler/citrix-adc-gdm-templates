# Google GDM templates for deploying Citrix VPX FIPS images

> Only standalone deployment is being supported for FIPS for now

## Steps to deploy:

1. Use any of our existing [standalone GDM templates](../standalone-templates).
2. change the `image_name` in `configuration.yml` file to `citrix-adc-vpx-fips-byol-12-1-latest`.
3. deploy the template.

> Instructions to deploy are present in standalone templates directories.

## Steps to configure VPX for FIPS-operating-mode:

1. Apply FIPS license files
	* Copy license files to `/nsconfig/license/` folder
2. Warm reboot the VPX
3. The CLI command `show fipsStatus` should show the below output.

``` bash
> show fipsStatus
	FipsStatus:  "System is operating in FIPS mode"
 Done
```

## Troubleshooting:

Please refer [here](https://docs.citrix.com/en-us/citrix-adc/12-1/ssl/citrix-adc-vpx-fips-appliances.html#troubleshooting)

## Further Reading:

1. [Citrix blogs - Citrix ADC VPX is now FIPS 140-2 Level 1 Certified](https://www.citrix.com/blogs/2020/12/07/citrix-adc-vpx-is-now-fips-140-2-level-1-certified/)
2. [Citrix Docs - Citrix ADC VPX FIPS certified appliances](https://docs.citrix.com/en-us/citrix-adc/12-1/ssl/citrix-adc-vpx-fips-appliances.html)

3. [Google Cloud - Citrix ADC VPX FIPS - Customer Licensed](https://console.cloud.google.com/marketplace/product/citrix-public/citrix-adc-vpx-fips-byol-solution?project=citrix-master-project&folder=&organizationId=)
