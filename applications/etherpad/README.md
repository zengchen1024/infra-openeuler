#Notes
Etherpad instance is located in os-infrastructure kubernetes cluster, since we
created VPC Peering, We can use service NodePort to proxy `etherpad.openuler.org` to
those pods.