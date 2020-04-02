# /etc/consul-vault.d/consul-vault.hcl
# Consul Agent configuration for Vault storage

datacenter          = "dc1"
log_level           = "INFO"
# advertise_addr      = "IP OF HOST"
# retry_join          = ["IP_OF_FIRST_CONSUL_SERVER", "IP_OF_SECOND_CONSUL_SERVER", "...", "...", "..."]
# encrypt = "USE THE SAME TOKEN FROM THE SERVER CONFIG"

# Uncomment to configure ACLs
# acl {
#   enabled        = true
#   default_policy = "allow"
#   enable_token_persistence = true
#   tokens {
#     agent  = "USE THE SAME TOKEN FROM THE SERVER CONFIG"
#   }
# }

# Overrides default Consul ports so we don't conflict with the service discovery agent
ports {
  http              = 7500
  dns               = -1
  server            = 7300
  serf_lan          = 7301
  serf_wan          = -1
}
