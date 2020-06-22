#Notes
Mailweb instances are located in openlookeng kubernetes cluster, since we
created VPC Peering, We can use service NodePort to proxy `mailweb.openlookeng.org` to
those pods.