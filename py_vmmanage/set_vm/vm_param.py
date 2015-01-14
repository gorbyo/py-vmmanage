__author__ = 'Oleh Horbachov'


def set_resource_pool(srv, env_param):
    env = ''
    resource_pools = dict(zip(srv.get_resource_pools().values(), srv.get_resource_pools().keys()))
    resource = "/Resources/"+env_param
    for k, v in resource_pools.iteritems():
        if resource == k:
            env = v
            break
        else:
            env = resource_pools.get("/Resources/Other")
    return env


def set_data_store(srv, ds_param):
    ds = ''
    for k, v in srv.get_datastores().iteritems():
        if ds_param == v:
            ds = k
            break
        else:
            ds = False
            break
    return ds