#Notes
Etherpad instance is located in os-infrastructure kubernetes cluster, since we
created VPC Peering, We can use service NodePort to proxy `etherpad.openlookeng.io` to
those pods.