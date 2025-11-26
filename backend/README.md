# API Contracts

## 1. Show conversations

### Description: Shows groups the user is a member of and the latest message sent or received with message details.

### Request:
#### Endpoint: GET/conversations

### Success Response:
#### Status: 200 OK 
#### Body:

```JSON
    [
    {
    "groupId": 12,
    "groupName": "Bit by Bit",
    "latestMessage": {
      "mesageId": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
      "senderName": "George",
      "messageContent": "Hey",
      "sentAt": "12-12-2024",
      "readStatus": True,
      }
    },
    {
    "groupId": 13,
    "groupName": "Pineapple on Pizza inc.",
    "latestMessage": {
      "mesageId": "914ea991-edef-11d1-a765-00a991ee6bf6"
      "senderName": "George",
      "messageContent": "Pineapple!",
      "sentAt": "12-12-2024",
      "readStatus": False,
      }
    },
    ]
```

## 2. Show messages

### Description: Show all messages sent in the group, including their message details.

### Request:
#### Endpoint: GET/messages


### Success Response:
#### Status: 200 OK
#### Body:

```JSON
  [
  {
    "messageId": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
    "senderName: "George",
    "messageContent": "Hey",
    "sentAt": 12-12-2024,
    "readStatus": True,
    "repliedTo": "f89d4fab-7ded-12d0-a765-00a0c91e6cf6"
  },
  { 
    "messageId": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
    "senderName: "George",
    "messageContent": "How are you?",
    "sentAt": 12-12-2024,
    "readStatus": True,
    "repliedTo": None,
  },
  ]
```
```
```


## 3. Send Message 

### Description: Send a message in the group.

### Request
#### Endpoint: POST/messages
#### Body: 

```JSON
{
  senderName: "George",
  messageContent: "Yo",
  sentAt: 12-12-2024,
  readStatus: True,
  repliedTo: None,
}
```

### Success Response
#### Status: 201 Created
#### Body:

```JSON
{
  messageId:"f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
  senderName: "George",
  messageContent: "Yo",
  sentAt: 12-12-2024,
  readStatus: True,
  repliedTo: None,

}
```
