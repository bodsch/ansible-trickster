
# Ansible Role:  `trickster`

[Trickster](https://github.com/tricksterproxy/trickster) ist an Open Source Dashboard Accelerator for Time Series Databases.

This ansible role installs and configure Trickster.

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-trickster/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-trickster)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-trickster)][releases]
[![Ansible Quality Score](https://img.shields.io/ansible/quality/50067?label=role%20quality)][quality]

[ci]: https://github.com/bodsch/ansible-trickster/actions
[issues]: https://github.com/bodsch/ansible-trickster/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-trickster/releases
[quality]: https://galaxy.ansible.com/bodsch/trickster

## Requirements & Dependencies

Ansible Collections

- [bodsch.core](https://github.com/bodsch/ansible-collection-core)
- [bodsch.scm](https://github.com/bodsch/ansible-collection-scm)

```bash
ansible-galaxy collection install bodsch.core
ansible-galaxy collection install bodsch.scm
```
or
```bash
ansible-galaxy collection install --requirements-file collections.yml
```


## Usage

Look to the [defaults](defaults/main.yml) properties file to see the possible configuration properties.

You can also look at the [molecule](molecule/default/group_vars/all) test.

### Operating systems

Tested on

* ArchLinux
* Debian based
    - Debian 10 / 11
    - Ubuntu 20.04

## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-trickster/tags)!

## Configuration

### main

```yaml
trickster_main:
  # default is 0, which means ignored
  instance_id: 0
  # default is /trickster/config
  config_handler_path: /trickster/config
  # default is /trickster/ping
  ping_handler_path: /trickster/ping
  # default is /trickster/health
  health_handler_path: /trickster/health
  # Options are: "metrics", "reload", "both", or "off"; default is both
  pprof_server: both
  # server_name defaults to os.Hostname() when left blank
  server_name: ''
```

### frontend

```yaml
trickster_frontend:
  # listen_port defines the port on which Tricksters Front-end HTTP Proxy server listens.
  listen_port: 8480
  # listen_address defines the ip on which Tricksters Front-end HTTP Proxy server listens.
  # empty by default, listening on all interfaces
  listen_address: ''
  # tls_listen_address defines the ip on which Tricksters Front-end TLS Proxy server listens.
  # empty by default, listening on all interfaces
  tls_listen_address: ''
  # tls_listen_port defines the port on which Tricksters Front-end TLS Proxy server listens.
  # The default is 0, which means TLS is not used, even if certificates are configured below.
  tls_listen_port: 0
  # connections_limit defines the maximum number of concurrent connections
  # Tricksters Proxy server may handle at any time.
  # 0 by default, unlimited.
  connections_limit: 0
```

### caches

[upstream](https://github.com/trickstercache/trickster/blob/main/examples/conf/example.full.yaml#L68-L190)

`provider` defines what kind of cache should be use.

options are `bbolt`, `badger`, `filesystem`, `memory` and `redis`

#### in-memory

```yaml
trickster_caches:
  default:
    provider: memory
```

#### redis

```yaml
trickster_caches:
  default:
    provider: redis
    redis:
      endpoint: 'redis:6379'
      endpoints:
        - redis:6379
      protocol: tcp
      db: 0
```

#### filesystem

```yaml
trickster_caches:
  default:
    provider: filesystem
    filesystem:
      cache_path: /var/cache/trickster
```

#### bbolt

```yaml
trickster_caches:
  default:
    provider: bbolt
    filename: trickster.db
    bucket: trickster
```

#### badger

```yaml
trickster_caches:
  default:
    provider: badger
    directory: /tmp/trickster
    value_directory: /tmp/trickster
```


### backends

[upstream](https://github.com/trickstercache/trickster/blob/main/examples/conf/example.full.yaml#L216-L524)

```yaml
trickster_backends:
  default:
    provider: prometheus
    is_default: true
    origin_url: http://prometheus:9090
```


### rules

```yaml


```


### request_rewriters

```yaml


```


### tracing

```yaml


```


### metrics

```yaml
trickster_metrics:
  listen_port: 8481
  listen_address: 127.0.0.1
```


### reloading

```yaml


```


### logging

```yaml
trickster_logging:
  # Possible values are 'debug', 'info', 'warn', 'error'
  log_level: warn
  log_file: /var/log/trickster.log
```

### example from upstream

[upstream doku](https://github.com/trickstercache/trickster/blob/main/examples/conf/example.full.yaml)


---

## Author and License

- Bodo Schulz

## License

This project is licensed under Apache License. See [LICENSE](/LICENSE) for more details.


**FREE SOFTWARE, HELL YEAH!**
