# BidulHouse
A gateway between Zabbix and a Telegram Bot to send a message when the fire alarm goes off.

## Zabbix Configuration
### Media
```
Name : BidulHouse
Type: Webhook
Parameters :
- Alert : {ALERT.SUBJECT}
- URL : http://localhost:8080/alerts
Script : (see below)
... (useless parameters)
Description : BidulHouse Alert Management
```
### Script
```javascript
try {
    var params = JSON.parse(value);

    var request = new CurlHttpRequest();
    request.AddHeader('Content-Type: application/json');

    return request.Post(params.URL, JSON.stringify({alert: params.Alert}));
}
catch (error) {
    Zabbix.Log(4, '[BidulHouse] notification failed: ' + error);
    throw '[BidulHouse] Sending failed: ' + error + '.';
}
```