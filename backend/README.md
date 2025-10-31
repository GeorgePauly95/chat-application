# API Contracts

## 1. Show groups
### Description: Shows groups the user is a member of and the latest message sent or received with message details.
### Request:

#### Endpoint: GET/conversations
#### Body:
```
{
  }
```

### Success Response:
#### Status: 200 OK 
#### Body:
```
    [
    {
    "groupId": 12,
    "groupName": "Bit by Bit",
    "latestMessage": {
    "mesageId": f81d4fae-7dec-11d0-a765-00a0c91e6bf6,
    "senderName": "George",
    "messageContent": "Hey",
    "sentAt": 12-12-2024,
    "readStatus": True,
    }
    },
    {
    "groupId": 13,
    "groupName": "Pineapple on Pizza inc.",
    "latestMessage": {
    "mesageId": 914ea991-edef-11d1-a765-00a991ee6bf6,
    "senderName": "George",
    "messageContent": "Pineapple!",
    "sentAt": 12-12-2024,
    "readStatus": False,
    }
    },
    ]
    ```


## 2. Show messages
### Descriptions: Show all messages sent in the group, including their message details.
### Request:

#### Endpoint: GET/messages
#### Body:
```
{

  }
```


### Success Response:
### Status: 200 OK
### Body:
```
  [
  {
    "mesageId": f81d4fae-7dec-11d0-a765-00a0c91e6bf6,
    "senderName: "George",
    "messageContent": "Hey",
    "sentAt": 12-12-2024,
    "readStatus": True,
    "repliedTo": f89d4fab-7ded-12d0-a765-00a0c91e6cf6,
  },
  { 
    "mesageId": f81d4fae-7dec-11d0-a765-00a0c91e6bf6,
    "senderName: "George",
    "messageContent": "How are you?",
    "sentAt": 12-12-2024,
    "readStatus": True,
    "repliedTo": None,
  },
  ]
```

