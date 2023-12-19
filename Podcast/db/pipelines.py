# In the name of GOD

RETRIVE_COMMENTS_PIPELINE = [
                    {"$lookup": 
                        {
                            "from": "comment_collection",
                            "localField": "comments",
                            "foreignField": "id",
                            "as" : "comments",
                            "pipeline":[
                                {"$project":
                                    {"_id":0,
                                    "username":1,
                                    "created_at": {
                                        "$dateToString": {
                                        "format": "%Y-%m-%d %H:%M:%S",
                                        "date": "$created_at"
                                        }},
                                    "text":1,
                                    }
                                },
                            ]

                        }
                    },
                    {"$project":
                        {
                        "_id":0,
                    }}
                ]