/*
Improve this later by allowing LoRa to send proper byte values instead of char *
*/
function decodeUplink(input) {
  
  // If delimiter 'A' is found, then note down the counter
  delimiterIdentity = 65;
  
  bytes = input.bytes;
  counter = 0;
  
  // Collect all parsed float values
  floatValues = [-1, -1, -1, -1];
  stringValues = ["", "", "", ""];
  index = 0;
  
  // Logic to split the bytes stream by the delimiter since this has NO inbuilt javascript libraries
  while (bytes.length !== 0 ){
    item = bytes[counter];
    if (item == delimiterIdentity){
      floatWord = bytes.slice(0, counter);
      stringValues[index] = String.fromCharCode.apply(null, floatWord);
      //floatValues = floatValues.concat([floatWord]);
      bytes = bytes.slice(counter+1); 
      counter = 0;
      index = index + 1;
    }
    counter = counter + 1;
    
  }
  
  return {data : {floatVALUES : stringValues }};
  for (const floatItem of floatValues){
    // floatItem is in bytes
    stringValues =  String.fromCharCode.apply(null, floatItem);
  }

// If the Input is of correct length and parsed correctly, only then send across to Flask, else drop it
  if (stringValues.length !== 4) {
    const pm25String = stringValues[0];
    const pm10String = stringValues[1];
    const temperatureString = stringValues[2];
    const humidityString = stringValues[3];
  

  return {
    data: {
    software_version : "test-imt-v0.1",
    sensordatavalues : [
      {
        value_type : "P2",
        value : pm25String
      },
      {
        value_type : "P1",
        value : pm10String
      },
      {
        value_type : "temperature",
        value : temperatureString
      },
      {
        value_type : "humidity",
        value : humidityString
      }
      ]
    }
  };
  
}
  
}
  
