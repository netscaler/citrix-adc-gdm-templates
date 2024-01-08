"""Creates Citrix ADC Three NIC deployment"""
COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'
def GenerateConfig(context):
  instance1_access_configs1 = [{
         'name': 'Management NAT',
         'type': 'ONE_TO_ONE_NAT',
         'natIP': '$(ref.static-external-instance1-mgmt-ip-' + context.env['deployment'] + '.address)'
  }]
  instance1_access_configs2 = [{
         'name': 'Management NAT',
         'type': 'ONE_TO_ONE_NAT',
         'natIP': '$(ref.static-external-instance1-traffic-ip-' + context.env['deployment'] + '.address)'
  }]
  instance2_access_configs = [{
         'name': 'Management NAT',
         'type': 'ONE_TO_ONE_NAT',
         'natIP': '$(ref.static-external-instance2-mgmt-ip-' + context.env['deployment'] + '.address)'
  }]
  #Primary Instance Network Interface Configuration
  instance1_network_interfaces = [{
      'network': ''.join([COMPUTE_URL_BASE, 'projects/',
                          context.env['project'], '/global/networks/',
                          context.properties['mgmt_network']]),
      'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                          context.env['project'], '/regions/',
                          context.properties['region'], '/subnetworks/',
                          context.properties['mgmt_subnet']]),
      'networkIP': '$(ref.static-internal-instance1-mgmt-ip-' + context.env['deployment'] + '.address)',
      'accessConfigs': instance1_access_configs1
      },
      {
      'network': ''.join([COMPUTE_URL_BASE, 'projects/',
                          context.env['project'], '/global/networks/',
                          context.properties['client_network']]),
      'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                          context.env['project'], '/regions/',
                          context.properties['region'], '/subnetworks/',
                          context.properties['client_subnet']]),
      'networkIP': '$(ref.static-internal-instance1-client-ip-' + context.env['deployment'] + '.address)',
      'accessConfigs': instance1_access_configs2
       },
       {
       'network': ''.join([COMPUTE_URL_BASE, 'projects/',
                           context.env['project'], '/global/networks/',
                           context.properties['server_network']]),
       'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                           context.env['project'], '/regions/',
                           context.properties['region'], '/subnetworks/',
                           context.properties['server_subnet']]),
       'networkIP': '$(ref.static-internal-instance1-server-ip-' + context.env['deployment'] + '.address)',
       'accessConfigs': []
        }]
  #Secondary Instance Network Interface Configuration
  instance2_network_interfaces = [{
      'network': ''.join([COMPUTE_URL_BASE, 'projects/',
                          context.env['project'], '/global/networks/',
                          context.properties['mgmt_network']]),
      'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                          context.env['project'], '/regions/',
                          context.properties['region'], '/subnetworks/',
                          context.properties['mgmt_subnet']]),
      'networkIP': '$(ref.static-internal-instance2-mgmt-ip-' + context.env['deployment'] + '.address)',
      'accessConfigs': instance2_access_configs
      },
      {
      'network': ''.join([COMPUTE_URL_BASE, 'projects/',
                          context.env['project'], '/global/networks/',
                          context.properties['client_network']]),
      'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                          context.env['project'], '/regions/',
                          context.properties['region'], '/subnetworks/',
                          context.properties['client_subnet']]),
      'networkIP': '$(ref.static-internal-instance2-client-ip-' + context.env['deployment'] + '.address)',
      'accessConfigs': []
       },
       {
       'network': ''.join([COMPUTE_URL_BASE, 'projects/',
                           context.env['project'], '/global/networks/',
                           context.properties['server_network']]),
       'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                           context.env['project'], '/regions/',
                           context.properties['region'], '/subnetworks/',
                           context.properties['server_subnet']]),
       'networkIP': '$(ref.static-internal-instance2-server-ip-' + context.env['deployment'] + '.address)',
       'accessConfigs': []
        }]

  if(context.properties['service_account'] != ""):
      service_accounts = [{
        'email': context.properties['service_account']
      }]
  else:
      service_accounts = [{
        'scopes': [
          'https://www.googleapis.com/auth/compute',
          'https://www.googleapis.com/auth/devstorage.read_only',
          'https://www.googleapis.com/auth/logging.write',
          'https://www.googleapis.com/auth/monitoring.write',
          'https://www.googleapis.com/auth/cloud-platform'
        ]
      }]

  if(context.properties['ssh_public_key'] != ""):
      ssh_keys = [{
        'key': 'ssh-keys',
        'value':context.properties['ssh_public_key']
      }]
  else:
      ssh_keys = []

  resources = [{
      'name': 'citrix-adc-instance1-' + context.env['deployment'],
      'type': 'compute.v1.instance',
      'properties': {
          'zone': context.properties['instance1_google_zone'],
          'machineType': ''.join([COMPUTE_URL_BASE, 'projects/',
                                  context.env['project'], '/zones/',
                                  context.properties['instance1_google_zone'], '/machineTypes/',
                                  context.properties['instance_type']]),
          'serviceAccounts': service_accounts,
          'disks': [{
              'deviceName': 'boot',
              'type': 'PERSISTENT',
              'boot': True,
              'autoDelete': True,
              'initializeParams': {
                  'sourceImage': ''.join([COMPUTE_URL_BASE, 'projects/' + context.properties['image_project_id'],
                                          '/global/images/',
                                          context.properties['image_name'],
                                         ])
              }
          }],
          'networkInterfaces': instance1_network_interfaces,
          'metadata': {
              'items': ssh_keys
          },
          'tags': {
            'items': ['mgmt-firewall-' + context.env['deployment'],
                      'client-firewall-' + context.env['deployment'],
                      'server-firewall-' + context.env['deployment']]
          },
		  'metadata': {
			'items': [{
				'key': 'peerIP',
				'value':'$(ref.static-internal-instance2-mgmt-ip-'+ context.env['deployment']+'.address)'
				}]
		}
      }
  },
  {
      'name': 'citrix-adc-instance2-' + context.env['deployment'],
      'type': 'compute.v1.instance',
      'properties': {
          'zone': context.properties['instance2_google_zone'],
          'machineType': ''.join([COMPUTE_URL_BASE, 'projects/',
                                  context.env['project'], '/zones/',
                                  context.properties['instance2_google_zone'], '/machineTypes/',
                                  context.properties['instance_type']]),
          'serviceAccounts': service_accounts,
          'disks': [{
              'deviceName': 'boot',
              'type': 'PERSISTENT',
              'boot': True,
              'autoDelete': True,
              'initializeParams': {
                  'sourceImage': ''.join([COMPUTE_URL_BASE, 'projects/' + context.properties['image_project_id'],
                                          '/global/images/',
                                          context.properties['image_name'],
                                         ])
              }
          }],
          'networkInterfaces': instance2_network_interfaces,
         # 'metadata': {
         #     'dependsOn': {
	 #        'items': 'citrix-adc-instance1-' + context.env['deployment']
	 #       }
         #  },
	  'metadata': {
              'items': ssh_keys
          },
          'tags': {
            'items': ['mgmt-firewall-' + context.env['deployment'],
                      'client-firewall-' + context.env['deployment'],
                      'server-firewall-' + context.env['deployment']]
          },
		  'metadata': {
			'items': [{
				'key': 'peerIP',
				'value':'$(ref.static-internal-instance1-mgmt-ip-'+ context.env['deployment']+'.address)'
				}]
		}
      }
  },
  {
    'name': 'mgmt-firewall-' + context.env['deployment'],
    'type': 'compute.v1.firewall',
    'properties': {
          'network': ''.join([COMPUTE_URL_BASE, 'projects/',
                            context.env['project'], '/global/networks/',
                            context.properties['mgmt_network']]),
          'sourceRanges': [context.properties['restricted_management_access_cidr']],
          'allowed': [{
              'IPProtocol': 'tcp',
              'ports': context.properties['mgmt_tcp_ports']
          },
          {
              'IPProtocol': 'udp',
              'ports': context.properties['mgmt_udp_ports']
          }],
          'direction': 'INGRESS',
          'priority': 1000
      }
  },
  {
    'name': 'client-firewall-' + context.env['deployment'],
    'type': 'compute.v1.firewall',
    'properties': {
          'network': ''.join([COMPUTE_URL_BASE, 'projects/',
                            context.env['project'], '/global/networks/',
                            context.properties['client_network']]),
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
              'IPProtocol': 'tcp',
              'ports': context.properties['traffic_ports']
          }],
          'direction': 'INGRESS',
          'priority': 1000
       }
  },
  {
    'name': 'server-firewall-' + context.env['deployment'],
    'type': 'compute.v1.firewall',
    'properties': {
          'network': ''.join([COMPUTE_URL_BASE, 'projects/',
                            context.env['project'], '/global/networks/',
                            context.properties['server_network']]),
          'sourceRanges': ['0.0.0.0/0'],
          'allowed': [{
              'IPProtocol': 'tcp',
              'ports': context.properties['traffic_ports']
          }],
          'direction': 'INGRESS',
          'priority': 1000
       }
  },
  {
    'name': 'static-internal-instance1-mgmt-ip-' + context.env['deployment'],
    'type': 'compute.v1.addresses',
    'properties': {
        'addressType': 'INTERNAL',
        'region': context.properties['region'],
        'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                            context.env['project'], '/regions/',
                            context.properties['region'], '/subnetworks/',
                            context.properties['mgmt_subnet']])
    }
  },
  {
    'name': 'static-internal-instance1-client-ip-' + context.env['deployment'],
    'type': 'compute.v1.addresses',
    'properties': {
        'addressType': 'INTERNAL',
        'region': context.properties['region'],
        'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                            context.env['project'], '/regions/',
                            context.properties['region'], '/subnetworks/',
                            context.properties['client_subnet']])

    }
  },
  {
    'name': 'static-internal-instance1-server-ip-' + context.env['deployment'],
    'type': 'compute.v1.addresses',
    'properties': {
        'addressType': 'INTERNAL',
        'region': context.properties['region'],
        'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                            context.env['project'], '/regions/',
                            context.properties['region'], '/subnetworks/',
                            context.properties['server_subnet']])
    }
  },
  {
    'name': 'static-internal-instance2-mgmt-ip-' + context.env['deployment'],
    'type': 'compute.v1.addresses',
    'properties': {
        'addressType': 'INTERNAL',
        'region': context.properties['region'],
        'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                            context.env['project'], '/regions/',
                            context.properties['region'], '/subnetworks/',
                            context.properties['mgmt_subnet']])
    }
  },
  {
    'name': 'static-internal-instance2-client-ip-' + context.env['deployment'],
    'type': 'compute.v1.addresses',
    'properties': {
        'addressType': 'INTERNAL',
        'region': context.properties['region'],
        'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                            context.env['project'], '/regions/',
                            context.properties['region'], '/subnetworks/',
                            context.properties['client_subnet']])

    }
  },
  {
    'name': 'static-internal-instance2-server-ip-' + context.env['deployment'],
    'type': 'compute.v1.addresses',
    'properties': {
        'addressType': 'INTERNAL',
        'region': context.properties['region'],
        'subnetwork': ''.join([COMPUTE_URL_BASE, 'projects/',
                            context.env['project'], '/regions/',
                            context.properties['region'], '/subnetworks/',
                            context.properties['server_subnet']])
    }
  },
  {
    'name': 'static-external-instance1-mgmt-ip-' + context.env['deployment'],
    'type': 'compute.v1.addresses',
    'properties': {
        'addressType': 'EXTERNAL',
        'region': context.properties['region']
    }
  },
  {
    'name': 'static-external-instance1-traffic-ip-' + context.env['deployment'],
    'type': 'compute.v1.addresses',
    'properties': {
        'addressType': 'EXTERNAL',
        'region': context.properties['region']
    }
  },
  {
    'name': 'static-external-instance2-mgmt-ip-' + context.env['deployment'],
    'type': 'compute.v1.addresses',
    'properties': {
        'addressType': 'EXTERNAL',
        'region': context.properties['region']
    }
  }]

  outputs = [
  {
    'name': 'citrx-adc-instance1-mgmt-external-ip',
    'value': '$(ref.citrix-adc-instance1-' + context.env['deployment'] + '.networkInterfaces[0].accessConfigs[0].natIP)'
  },
  {
    'name': 'citrix-adc-instance1-client-external-ip',
    'value': '$(ref.citrix-adc-instance1-' + context.env['deployment'] + '.networkInterfaces[1].accessConfigs[0].natIP)'

  },
  {
    'name': 'citrix-adc-instance1-server-internal-ip',
    'value': '$(ref.citrix-adc-instance1-' + context.env['deployment'] + '.networkInterfaces[2].networkIP)'

  },
  {
    'name': 'citrix-adc-instance2-mgmt-external-ip',
    'value': '$(ref.citrix-adc-instance1-' + context.env['deployment'] + '.networkInterfaces[2].networkIP)'

  },
  {
    'name': 'citrix-adc-instance2-client-internal-ip',
    'value': '$(ref.citrix-adc-instance1-' + context.env['deployment'] + '.networkInterfaces[2].networkIP)'

  },
  {
    'name': 'citrix-adc-instance2-server-internal-ip',
    'value': '$(ref.citrix-adc-instance1-' + context.env['deployment'] + '.networkInterfaces[2].networkIP)'

  }]

  return {'resources': resources, "outputs": outputs}
