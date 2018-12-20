# based on https://pypi.org/project/osmapi/ and http://osmapi.metaodi.ch/#header-classes
# not a built-in library in PyCharm
import osmapi

# I made an account for us to all use
# api = osmapi.OsmApi(api="https://api06.dev.openstreetmap.org", username="OSM_buildingdetector", password="fakepassword123")

def sign_in(api, username, password):
    api = osmapi.OsmApi(api=api, username=username, password=password)
    return api

# tag must be as a dict, like {"Corner": "1"}
def node_create(api, latitude, longitude, comment, tag = {}):
    node = api.NodeCreate({"lat": latitude, "lon": longitude, "tag": tag})
    return node

# tag must be as a dict, like {"Way": "The best way!"}
# default is tagless
def way_create(api, node_list, comment, tag = {}):
    # add meaningful comments pls :)
    api.ChangesetCreate({u"comment": comment})

    # make Nodes based on longitude and latitude
    # add relevant tags
    # example code, REMOVE LATER
    # Node1 = api.NodeCreate({"lat": 41.788348, "lon": -88.129079, "tag": {"Corner": "1"}})
    # Node2 = api.NodeCreate({"lat": 41.788453, "lon": -88.129079, "tag": {"Corner": "2"}})
    # Node3 = api.NodeCreate({"lat": 41.788445, "lon": -88.129262, "tag": {"Corner": "3"}})
    # Node4 = api.NodeCreate({"lat": 41.788338, "lon": -88.129211, "tag": {"Corner": "4"}})

    # need the id of the Node specifically
    # node_list = [Node1["id"], Node2["id"], Node3["id"], Node4["id"]]

    # create the way (area) using the nodes
    # add relevant tag
    # way = api.WayCreate({"nd": node_list, "tag": {}})

    node_id_list = []
    for node in node_list:
        node_id_list.append(node["id"])

    way = api.WayCreate({"nd": node_id_list, "tag": tag})

    # close set of changes
    api.ChangesetClose()
    return way

# Create a changeset with multiple ways (multiple buildings)
def way_create_multiple(api, all_rects_dict, comment, tag = {"building": "yes"}):
    # Create the changeset
    api.ChangesetCreate({u"comment": comment})
    
    way_list = []
    
    # Create each way
    for rect in all_rects_dict.values():
        node_list = []
        
        for coordinates in rect:
            lat = coordinates[0]
            long = coordinates[1]
            node = node_create(api, lat, long, "")
            node_list.append(node["id"])
        
        # If there are at least three nodes, create the area
        if len(node_list) >= 3:
            node_list.append(node_list[0])
            this_way = api.WayCreate({"nd": node_list, "tag": tag})
            way_list.append(this_way)
    
    # Close the changeset
    api.ChangesetClose()
    return way_list

def find_way(api, way):
    # see data on the way you just made
    return api.WayGet(str(way["id"]))

# how code should be called
# api = sign_in()
# Node1 = node_create(api, 41.788348, -88.129079, "Node 1", {"Corner": "1"})
# Node2 = node_create(api, 41.788453, -88.129079, "Node 2", {"Corner": "2"})
# Node3 = node_create(api, 41.788445, -88.129262, "Node 3", {"Corner": "3"})
# Node4 = node_create(api, 41.788338, -88.129211, "Node 4", {"Corner": "4"})
# node_list = [Node1, Node2, Node3, Node4]
# way = way_create(api, node_list, "test")
# print(find_way(api, way))
