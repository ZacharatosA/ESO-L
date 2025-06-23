#Orion CB
#SELECT * FROM etv1 WHERE entity_id = 'urn:ngsi-ld:Store:001';
#curl -X POST 'http://localhost:4200/_sql?pretty' -H 'Content-Type: application/json' -d '{"stmt": "SELECT * FROM etstore LIMIT 10"}'

# FIWARE Configuration
FIWARE_SERVICE="BPO"
FIWARE_SERVICEPATH="v1"

# Current fiware-service {iot_ul}
# Current fiware-servicepath  {Dummy, pc_sensor , training_data}

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
JSON_DIR="${SCRIPT_DIR}/Fiware_config/Jsons"

alias export_cb_ent= "curl -s "http://localhost:1026/v2/entities" | jq -r '.[].id' > entities.txt"
alias get-cb-ent="curl -X GET 'http://localhost:1026/v2/entities' |jq"
alias get-cb-${FIWARE_SERVICE}="curl -X GET 'http://localhost:1026/v2/entities' \
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}' | jq"
alias del-cb-ent="curl -X DELETE 'http://localhost:1026/v2/entities/ModbusDevice:002' \
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}'"
#Subscription----------------------------------------------------------------------------------
alias post-subs="curl -X POST 'http://localhost:1026/v2/subscriptions' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}' \
  -d @${JSON_DIR}/subscriptions.json"
alias get-subs="curl -X GET 'http://localhost:1026/v2/subscriptions'\
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}'  |jq"
alias del-sub="curl -X DELETE 'http://localhost:1026/v2/subscriptions/684c3885680cf45b0502a52e' \
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}'"

#IoT Agent UL-------------------------------------------------------------------------------
alias check-ul="curl -X GET 'http://localhost:4061/iot/about' |jq"
#services---------------
alias get-serv="curl -X GET 'http://localhost:4061/iot/services'   -H 'Content-Type: application/json' \
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}' \ | jq"
alias post-serv="curl -X POST 'http://localhost:4061/iot/services' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}' \
  -d @${JSON_DIR}/services_inf_sens.json"
alias del-serv="curl -iX DELETE \
  'http://localhost:4061/iot/services/?resource=/iot/d&apikey=inferencekey' \
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}'"
#Devices-------------------
alias get-dev="curl -X GET 'http://localhost:4061/iot/devices' -H 'Content-Type: application/json' \
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}'| jq"
alias post-dev="curl -X POST 'http://localhost:4061/iot/devices' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}' \
  -d @${JSON_DIR}/devices.json"
alias del-dev="curl -X DELETE 'http://localhost:4061/iot/devices/TempSensor' \
  -H 'fiware-service: ${FIWARE_SERVICE}' \
  -H 'fiware-servicepath: /${FIWARE_SERVICEPATH}'"

#Dummy Devices comunication
alias dummy-sensor="curl -X POST 'http://localhost:7896/iot/d?k=dummyulkey&i=sensor001' -H 'Content-Type: text/plain' -d 't|25.3'"

#-------------------------Crate_DB------------------------------------------

#------------------------Security-----------------------------------------
alias admin-token="curl -k -iX POST \
  'https://localhost:3443/v1/auth/tokens' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "azach@test.com",
    "password": "azach1234"
  }'"