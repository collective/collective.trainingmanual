=====================
Monitoring avec Munin
=====================
Installez le serveur et le client Munin : ::

    apt-get install munin munin-node

À l'installation il active les plugins suivants : ::

    apache_processes cpu df df_inode entropy forks if_err_eth0 if_err_eth1 if_eth0 if_eth1 interrupts iostat irqstats load memory mysql_bytes mysql_queries mysql_slowqueries mysql_threads netstat open_files open_inodes postfix_mailqueue postfix_mailvolume processes smart_sda smart_sdb swap vmstat

Éditez /etc/munin/munin.conf : ::

    # a simple host tree
    [host.domain.com]
        address 127.0.0.1
        use_node_name yes

Rechargez le fichier de configuration : ::

    /usr/share/munin/munin-update --force-root

vi /etc/munin/munin-node.conf

Changer en :
::

    host 127.0.0.1

Redémarrer::

    /etc/init.d/munin-node restart

Exemple de buildout de deploiement avec munin : ::

    [buildout]
    extends = buildout.cfg
    parts +=
        zeoserver
        instance1
        instance2
        munin1

    [hosts]
    zeoserver   = 127.0.0.1
    instance1   = 127.0.0.1
    instance2   = 127.0.0.1

    [ports]
    zeoserver   = 8100
    instance1   = 9880
    instance2   = 9881

    [instance-settings]
    eggs =
        ${instance:eggs}
        munin.zope
    zcml =
        ${instance:zcml}
        munin.zope
    products = ${instance:products}
    user = ${instance:user}
    zodb-cache-size = 8000
    zeo-client-cache-size = 300MB
    debug-mode = off
    zope2-location = ${zope2:location}
    zeo-client = true
    zeo-address = ${zeoserver:zeo-address}
    effective-user = ${users:zope}
    environment-vars = ${instance:environment-vars}
    zserver-threads = 2

    [instance1]
    recipe = collective.recipe.zope2cluster
    instance-clone = instance-settings
    http-address = ${hosts:instance1}:${ports:instance1}

    [instance2]
    recipe = collective.recipe.zope2cluster
    instance-clone = instance-settings
    http-address = ${hosts:instance2}:${ports:instance2}

    [munin1]
    recipe = zc.recipe.egg
    eggs = munin.zope
    scripts = munin=munin1
    arguments = ip_address='${hosts:instance1}', http_address='${ports:instance1}', user='${instance1:user}'

    [munin2]
    recipe = zc.recipe.egg
    eggs = munin.zope
    scripts = munin=munin2
    arguments = ip_address='${hosts:instance2}', http_address='${ports:instance2}', user="${instance2:user}"

Installez les liens symboliques : ::

    >>> sudo ./bin/munin1 install /etc/munin/plugins instance1
    installed symlink /etc/munin/plugins/instance1_zopecache_plonesite
    installed symlink /etc/munin/plugins/instance1_zopememory_plonesite
    installed symlink /etc/munin/plugins/instance1_zodbactivity_plonesite
    installed symlink /etc/munin/plugins/instance1_zopethreads_plonesite
    >>> sudo ./bin/munin2 install /etc/munin/plugins instance2
    installed symlink /etc/munin/plugins/instance2_zopecache_plonesite
    installed symlink /etc/munin/plugins/instance2_zopememory_plonesite
    installed symlink /etc/munin/plugins/instance2_zodbactivity_plonesite
    installed symlink /etc/munin/plugins/instance2_zopethreads_plonesite


Ressources
==========

- http://www.debianadmin.com/monitor-servers-and-clients-using-munin-in-ubuntu.htm
- http://www.debianhelp.co.uk/munin.htm
- http://www.debuntu.org/how-to-monitoring-a-server-with-munin
- http://www.debuntu.org/how-to-monitoring-a-server-with-munin-p2

