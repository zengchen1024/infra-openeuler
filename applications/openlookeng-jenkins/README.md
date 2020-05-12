#Notes
Jenkins master instance is located in openlookeng kubernetes cluster, since we
created VPC Peering, We can use service NodePort to proxy `build.openlookeng.org` to
those pods.