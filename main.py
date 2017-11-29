#!/usr/bin/python
#
# (c) 2017, Martyn Pratt <martynjamespratt@gmail.com>
# MIT License 


import requests

class base(object):
    def __error__(self, message):
        """
        Base error function
        :param message: the message to be displayed before exiting
        """
        print("ERROR:" + message)
        exit(1)

class client(base):
    def __init__(self, base_url="https://notdb.martyni.co.uk"):
        self.base_url = base_url
    
    def base_request(self, db, thing, index=None, req_type="GET", thing_type="thing", payload=None):
        """
        Base request function
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :param index: If the thing is a list an index can be specified
        :param req_type: choices= GET, POST, PUT, DEL 
        :param thing_type: choices= thing, list, link, file
        :param payload: When posting this needs to be set to a json compatible dictionary
        :return: raw request response
        """
        func_dict ={
                "GET":requests.get,
                "POST": requests.post,
                "PUT": requests.put,
                "DEL": requests.delete
                }
        
        try:
           if index is None:
              url = "{}/{}/{}/{}".format(
              self.base_url,
              db,
              thing_type,
              thing
              ) 
           else:
              url = "{}/{}/{}/{}/{}".format(
              self.base_url,
              db,
              thing_type,
              thing,
              index
              ) 
           if payload is None:
              self.response = func_dict[req_type](url)
           else:
              self.response = func_dict[req_type](url, json=payload)
        except:
           self.__error__("Accepted types are GET, POST, PUT or DEL. Not {}".format(req_type))
        return self.response

    def __get(self, db, thing, thing_type, index=None):
        """
        Base get function
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :param thing_type: choices= thing, list, link, file
        :param index: If the thing is a list an index can be specified
        :return: dictionary containing json payload
        """
        if index is not None:
           return self.base_request(db, thing, index=index, thing_type=thing_type)
        else:
           return self.base_request(db, thing, thing_type=thing_type)

    def __delete(self, db, thing, thing_type, index=None):
        """
        Base delete function
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :param thing_type: choices= thing, list, link, file
        :param index: If the thing is a list an index can be specified
        :return: None if succesfull 
        """
        if index is not None:
           return self.base_request(db, thing, index=index, thing_type=thing_type, req_type="DEL")
        else:
           return self.base_request(db, thing, thing_type=thing_type, req_type="DEL")

    def __post(self, db, thing, thing_type, payload, index=None):
        """
        Base post function
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :param thing_type: choices= thing, list, link, file
        :param payload: json compatible dictionary
        :param index: If the thing is a list an index can be specified
        :return: dictionary containing json payload
        """
        if index is not None:
           return self.base_request(db, thing, index=index, thing_type=thing_type, req_type="POST", payload=payload)
        else:
           return self.base_request(db, thing, thing_type=thing_type, req_type="POST",payload=payload)

    def get_thing(self, db, thing):
        """
        get thing
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :return: dictionary containing json payload
        """
        return self.__get(db, thing, "thing").json()
           
    def get_list(self, db, thing):
        """
        get list
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :return: list containing enpoints of items in list
        """
        return self.__get(db, thing, "list").json()

    def get_item(self, db, thing, index):
        """
        get item
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :param index: index position of item
        :return: dictionary containing json payload
        """
        return self.__get(db, thing, "list", index=index).json()

    def delete_thing(self, db, thing):
        """
        delete thing
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        """
        return self.__delete(db, thing, "thing").json()
           
    def delete_list(self, db, thing):
        """
        delete list
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        """
        return self.__delete(db, thing, "list").json()

    def delete_item(self, db, thing, index):
        """
        delete item
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :param index: If the thing is a list an index can be specified
        """
        return self.__delete(db, thing, "list", index=index).json()

    def post_thing(self, db, thing, payload):
        """
        post item
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :param payload: json compatible dictionary 
        :return: dictionary containing json payload
        """
        return self.__post(db, thing, "thing", payload=payload).json()
           
    def append_list(self, db, thing, payload):
        """
        append item to list
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :param payload: json compatible dictionary 
        :return: newly appended list
        """
        return self.__post(db, thing, "list", payload=payload).json()

    def post_item(self, db, thing, index, payload):
        """
        delete item
        :param db: Database the thing is contained in
        :param thing: Name of the thing
        :param index: If the thing is a list an index can be specified
        :return: dictionary containing json payload
        """
        return self.__post(db, thing, "list", index=index, payload=payload).json()
