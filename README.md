# argus
A storage monitoring tool for CDAC's High Performance Computing systems

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
![forthebadge made-with-python](https://forthebadge.com/images/badges/powered-by-black-magic.svg)

[![HitCount](http://hits.dwyl.com/sakshatshinde/argus.svg)](http://hits.dwyl.com/sakshatshinde/argus)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues) 
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ea81086bdefa4876a38f68fe3a2942bb)](https://app.codacy.com/manual/sakshatshinde/argus?utm_source=github.com&utm_medium=referral&utm_content=sakshatshinde/argus&utm_campaign=Badge_Grade_Settings)

- ## Grafana Dashboard
![Image](grafana_argus_cdac.png)

- ## Metrics Collector
![Image](metrics_collector.png)

- ## Firebase
![Image](remote_db_cdac_argus.png)

# Install the following dependencies
  - Install python req: `pip install -r requirements.txt`
  - Install memcached:`sudo apt install memcached libmemcached-tools` (for debian)
  -  [Grafana](https://grafana.com/docs/grafana/latest/installation/)
  -  [MySQL](https://dev.mysql.com/downloads/installer/)
  - Setup a database in [Firebase](https://firebase.google.com/)
  
### Usage

Start memcached service
```sh
$ memcached
```

Create the table in MySQL instance
```sh 
$ \connect root@localhost:3306
```

```sh
CREATE DATABASE cdac_argus;
```

```sh 
$ use cdac_argus;
```
Database command to create the table
```sh
CREATE TABLE cachestat( metric_id INT NOT NULL AUTO_INCREMENT, buffers_mb INT NOT NULL, cached_mb INT NOT NULL, hits INT NOT NULL, mbd INT NOT NULL, misses INT NOT NULL, ratio INT NOT NULL, PRIMARY KEY ( metric_id ) );
```

```sh
$ SHOW TABLES;
```

Start the grafana service
> `Make sure you have setup the MySQL db correctly as it is required to be the datasource for Grafana`

> Open `localhost:3000` for opening the grafana dashboard

> NOTE: `If you change the installation settings the port might be different for grafana`

> Click on `CREATE`/ `+` symbol and click `import`

> In the `Import via panel json` section paste the code from `grafana_dashboard.json` from this repository

#### Running the metrics collector
```sh
$ sudo python cachestat.py
$ sudo python retrieve_data.py
```

#### About the firebase instance

> Make sure to make all the necessary changes in the code and use your own firebase db

> An example firebase url: https://cdac-argus-default-rtdb.firebaseio.com/


